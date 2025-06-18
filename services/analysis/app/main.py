from __future__ import annotations

import os
import threading
from typing import Dict, List

import networkx as nx
import numpy as np
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sklearn.ensemble import RandomForestClassifier

from libs.agentsdk import subscribe

# ----------------------------------------------------------------------------
# Application setup
# ----------------------------------------------------------------------------
app = FastAPI()
graph = nx.DiGraph()
# list of tuples (path, score)
top_paths: List[Dict[str, float]] = []

# simple model trained on dummy data so predict_proba works
_model = RandomForestClassifier(n_estimators=10, random_state=42)
# Train on simple two-class data so predict_proba returns two columns
_model.fit([[1, 1.0], [2, 2.0]], [0, 1])


def update_graph(alert: Dict) -> None:
    """Update graph nodes and edges from a classified alert and recompute paths."""
    technique = alert.get("technique_id")
    asset = alert.get("asset_id")
    tech_node = f"tech:{technique}"
    asset_node = f"asset:{asset}"
    graph.add_node(tech_node, type="technique")
    graph.add_node(asset_node, type="asset")
    weight = graph[asset_node][tech_node]["weight"] + 1 if graph.has_edge(asset_node, tech_node) else 1
    graph.add_edge(asset_node, tech_node, weight=weight)
    compute_top_paths()


def compute_top_paths() -> None:
    """Compute and ML-rerank the top 5 shortest paths."""
    paths = []
    assets = [n for n, d in graph.nodes(data=True) if d.get("type") == "asset"]
    techniques = [n for n, d in graph.nodes(data=True) if d.get("type") == "technique"]
    for a in assets:
        for t in techniques:
            if nx.has_path(graph, a, t):
                path = nx.dijkstra_path(
                    graph, a, t, weight=lambda u, v, d: 1 / d["weight"]
                )
                cost = nx.dijkstra_path_length(
                    graph, a, t, weight=lambda u, v, d: 1 / d["weight"]
                )
                paths.append((path, cost))
    paths.sort(key=lambda x: x[1])
    candidates = paths[:5]
    if not candidates:
        top_paths.clear()
        return
    features = [
        [len(p), np.mean([graph[p[i]][p[i+1]]["weight"] for i in range(len(p)-1)])]
        for p, _ in candidates
    ]
    scores = _model.predict_proba(features)[:, 1]
    ranked = sorted(zip(candidates, scores), key=lambda x: x[1], reverse=True)
    top_paths[:] = [{"path": p, "score": float(score)} for (p, _), score in ranked]


def _listen() -> None:
    for alert in subscribe("alerts"):
        update_graph(alert)

# ----------------------------------------------------------------------------
# Lifespan (startup/shutdown) handler
# ----------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    if os.getenv("NO_KAFKA") != "1":
        thread = threading.Thread(target=_listen, daemon=True)
        thread.start()

    yield

    
# ----------------------------------------------------------------------------
# Attach lifespan to app
# ----------------------------------------------------------------------------
app = FastAPI(lifespan=lifespan)

@app.get("/top-paths")
async def get_top_paths() -> List[Dict]:
    return top_paths

if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("ANALYSIS_PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
