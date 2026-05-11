"""
OSagnent Observe Layer — Hermes Pre/Post Tool Hook Plugin
===========================================================
Tracks all tool calls to build observation logs for worker pattern learning.

Hooks into: pre_tool_call, post_tool_call, on_session_finalize
Stores to: ~/.hermes/osagnent/observations/<worker_id>/<session_id>.jsonl
"""
from __future__ import annotations
import json, time, uuid
from pathlib import Path
from typing import Optional, Any

DATA_DIR = Path.home() / ".hermes" / "osagnent" / "observations"

class WorkerObserver:
    def __init__(self, worker_id: str = "default"):
        self.worker_id = worker_id
        self.session_id = str(uuid.uuid4())[:8]
        self.data_dir = DATA_DIR / worker_id
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.pending_actions: list[dict] = []
        self.completed_actions: list[dict] = []
        self.decisions: list[dict] = []
        self.confidence_samples: list[dict] = []

    def log_event(self, event_type: str, data: dict):
        path = self.data_dir / f"{self.session_id}.jsonl"
        with open(path, "a") as f:
            f.write(json.dumps({"ts": time.time(), "type": event_type, **data}) + "\n")

    def on_pre_tool(self, tool_name: str, args: dict, session_id: str, task_id: str):
        self.log_event("pre_tool", {
            "tool": tool_name,
            "args": args,
            "session": session_id,
            "task": task_id
        })
        self.pending_actions.append({"tool": tool_name, "args": args, "ts": time.time()})

    def on_post_tool(self, tool_name: str, args: dict, result: str, session_id: str, task_id: str, duration_ms: float):
        # Find matching pre-tool or mark as autonomous
        action = self.pending_actions.pop(0) if self.pending_actions else {"tool": tool_name, "args": args}
        self.log_event("post_tool", {
            "tool": tool_name,
            "args": action["args"],
            "result_hash": str(hash(result))[:16] if result else None,
            "duration_ms": duration_ms,
            "session": session_id,
            "task": task_id,
            "outcome": "success" if result else "failure"
        })
        self.completed_actions.append({**action, "duration_ms": duration_ms})

    def on_decision(self, context: str, decision: str, confidence: float, session_id: str):
        self.log_event("decision", {
            "context": context,
            "decision": decision,
            "confidence": confidence,
            "session": session_id
        })
        self.decisions.append({"context": context, "decision": decision, "confidence": confidence})

    def on_human_approval(self, task_id: str, approved: bool, feedback: str, session_id: str):
        self.log_event("approval", {
            "task": task_id,
            "approved": approved,
            "feedback": feedback,
            "session": session_id
        })
        # Update confidence stats
        confidence = 1.0 if approved else 0.0
        self.confidence_samples.append({"task": task_id, "confidence": confidence, "ts": time.time()})

    def get_confidence(self) -> float:
        if not self.confidence_samples:
            return 0.5  # Start neutral
        recent = [s["confidence"] for s in self.confidence_samples[-20:]]
        return sum(recent) / len(recent)

    def generate_report(self) -> dict:
        return {
            "worker_id": self.worker_id,
            "session_id": self.session_id,
            "total_actions": len(self.completed_actions),
            "decisions": len(self.decisions),
            "confidence": self.get_confidence(),
            "tools_used": list(set(a["tool"] for a in self.completed_actions)),
            "top_decisions": sorted(self.decisions, key=lambda d: d["confidence"])[:5]
        }

def register(ctx):
    ctx.register_tool("osagnent_observe", {
        "session_start": WorkerObserver,
        "pre_tool": lambda o, **kw: o.on_pre_tool(**kw),
        "post_tool": lambda o, **kw: o.on_post_tool(**kw),
        "decision": lambda o, **kw: o.on_decision(**kw),
        "approval": lambda o, **kw: o.on_human_approval(**kw),
        "report": lambda o: o.generate_report()
    })
