from __future__ import annotations

import os
import threading
from typing import Dict

import networkx as nx
from fastapi import FastAPI

from agentsdk import subscribe

app = FastAPI()
graph = nx.DiGraph()


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


def _listen() -> None:
    for alert in subscribe("alerts"):
        update_graph(alert)


@app.on_event("startup")
def startup_event() -> None:
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
