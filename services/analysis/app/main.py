from __future__ import annotations

import os
from typing import Any, List

import networkx as nx
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# in-memory directed graph
graph = nx.DiGraph()


class Edge(BaseModel):
    source: str
    target: str
    weight: float = 1.0


@app.post("/analysis/edge")
async def add_edge(edge: Edge) -> dict[str, Any]:
    """Add an edge to the analysis graph."""
    graph.add_edge(edge.source, edge.target, weight=edge.weight)
    return {"status": "edge_added", "edges": graph.number_of_edges()}


@app.get("/analysis/path")
async def get_paths(source: str, target: str, k: int = 5) -> dict[str, Any]:
    """Return up to k shortest paths between source and target."""
    if not graph.has_node(source) or not graph.has_node(target):
        raise HTTPException(status_code=404, detail="source or target not found")

    paths_iter = nx.shortest_simple_paths(graph, source, target, weight="weight")
    paths = []
    for i, p in enumerate(paths_iter):
        if i >= k:
            break
        weight = nx.path_weight(graph, p, weight="weight")
        paths.append({"nodes": p, "weight": weight})
    return {"paths": paths}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("ANALYSIS_PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
