from __future__ import annotations

import os
import sqlite3
import threading
from typing import Dict

import networkx as nx
from fastapi import FastAPI

from agentsdk import subscribe
from attackkit import AttackParser

app = FastAPI()
graph = nx.DiGraph()
db_path = os.getenv("GRAPH_DB", "graph.db")
conn = sqlite3.connect(db_path, check_same_thread=False)


def init_db() -> None:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS edges (source TEXT, target TEXT, weight INTEGER, PRIMARY KEY (source, target))"
    )
    conn.commit()


def load_graph() -> None:
    for src, tgt, wt in conn.execute("SELECT source, target, weight FROM edges"):
        graph.add_node(src)
        graph.add_node(tgt)
        graph.add_edge(src, tgt, weight=wt)

    path = os.getenv("ATTACK_JSON")
    if path:
        parser = AttackParser(path)
        for tid in parser.get_techniques():
            graph.add_node(f"tech:{tid}", type="technique")


def update_graph(alert: Dict) -> None:
    """Update graph nodes and edges from a classified alert."""
    technique = alert.get("technique_id")
    asset = alert.get("asset_id")
    tech_node = f"tech:{technique}"
    asset_node = f"asset:{asset}"
    graph.add_node(tech_node, type="technique")
    graph.add_node(asset_node, type="asset")
    weight = 1
    if graph.has_edge(asset_node, tech_node):
        weight = graph[asset_node][tech_node]["weight"] + 1
    graph.add_edge(asset_node, tech_node, weight=weight)
    conn.execute(
        "INSERT INTO edges (source, target, weight) VALUES (?, ?, ?) "
        "ON CONFLICT(source, target) DO UPDATE SET weight=excluded.weight",
        (asset_node, tech_node, weight),
    )
    conn.commit()


def _listen() -> None:
    for alert in subscribe("alerts"):
        update_graph(alert)


@app.on_event("startup")
def startup_event() -> None:
    init_db()
    load_graph()
    if os.getenv("NO_KAFKA") != "1":
        thread = threading.Thread(target=_listen, daemon=True)
        thread.start()


@app.get("/nodes")
def get_nodes() -> list:
    return list(graph.nodes())


@app.get("/edges")
def get_edges() -> list:
    return [
        {"source": u, "target": v, "weight": d["weight"]}
        for u, v, d in graph.edges(data=True)
    ]


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("GRAPH_PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
