from __future__ import annotations

import os
from typing import Any

import networkx as nx
from fastapi import FastAPI
from pydantic import BaseModel

from attackkit import AttackParser

app = FastAPI()

graph = nx.DiGraph()

attack_path = os.getenv("ATTACK_JSON_PATH")
if attack_path:
    parser = AttackParser(attack_path)
    for tid in parser.get_techniques():
        graph.add_node(tid)


class EdgeUpdate(BaseModel):
    source: str
    target: str
    weight: float = 1.0


@app.post("/graph/update")
async def update_graph(update: EdgeUpdate) -> dict[str, Any]:
    graph.add_edge(update.source, update.target, weight=update.weight)
    return {"status": "updated", "edges": graph.number_of_edges()}


@app.get("/graph")
async def read_graph() -> dict[str, Any]:
    return nx.readwrite.json_graph.node_link_data(graph)


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("GRAPH_PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
