"""
OSagnent Pattern Engine
=======================
Reads observation logs, groups them into task workflows, scores confidence.

Input: ~/.hermes/osagnent/observations/<worker_id>/*.jsonl
Output: ~/.hermes/osagnent/patterns/<worker_id>/tasks.json
"""
from __future__ import annotations
import json, time
from pathlib import Path
from collections import defaultdict
from typing import Optional

OBS_DIR = Path.home() / ".hermes" / "osagnent" / "observations"
PATTERN_DIR = Path.home() / ".hermes" / "osagnent" / "patterns"

def load_observations(worker_id: str) -> list[dict]:
    obs_dir = OBS_DIR / worker_id
    if not obs_dir.exists():
        return []
    events = []
    for f in obs_dir.glob("*.jsonl"):
        with open(f) as fh:
            for line in fh:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
    return sorted(events, key=lambda e: e.get("ts", 0))

def build_tasks(worker_id: str) -> list[dict]:
    events = load_observations(worker_id)
    pre_tools = [e for e in events if e["type"] == "pre_tool"]
    tool_usage = defaultdict(int)
    for e in pre_tools:
        tool_usage[e["tool"]] += 1
    
    # Group sequential tools into task clusters
    tasks = []
    current_task = None
    for e in pre_tools:
        if current_task is None:
            current_task = {"id": f"task_{len(tasks)+1}", "steps": [], "confidence": 0.5}
        current_task["steps"].append({
            "tool": e["tool"],
            "args": e["args"],
            "ts": e["ts"]
        })
        # New task cluster if gap > 5 min
        if len(current_task["steps"]) > 1:
            gap = e["ts"] - current_task["steps"][-2]["ts"]
            if gap > 300:
                tasks.append(current_task)
                current_task = None
    if current_task and current_task["steps"]:
        tasks.append(current_task)
    
    # Calculate task frequencies
    task_counts = defaultdict(int)
    for task in tasks:
        step_signature = ",".join(s["tool"] for s in task["steps"])
        task_counts[step_signature] += 1
    
    # Assign confidence based on frequency
    for task in tasks:
        sig = ",".join(s["tool"] for s in task["steps"])
        freq = task_counts[sig]
        task["confidence"] = min(0.5 + (freq * 0.05), 0.95)  # Max 95% until human approval
        task["frequency"] = freq
        task["tools_used"] = list(set(s["tool"] for s in task["steps"]))
    
    return tasks

def get_top_tasks(worker_id: str, top_n: int = 10) -> list[dict]:
    tasks = build_tasks(worker_id)
    return sorted(tasks, key=lambda t: t.get("frequency", 0), reverse=True)[:top_n]

def generate_pattern_report(worker_id: str) -> dict:
    tasks = get_top_tasks(worker_id, 20)
    all_tools = set()
    for t in tasks:
        all_tools.update(t.get("tools_used", []))
    return {
        "worker_id": worker_id,
        "total_sessions": len(set(t.get("session", "unknown") for t in load_observations(worker_id))),
        "unique_tasks": len(tasks),
        "top_tasks": tasks,
        "all_tools_used": list(all_tools),
        "generated_at": time.time()
    }
