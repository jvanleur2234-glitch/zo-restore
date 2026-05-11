"""Batch learning from multiple observation sessions."""
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import here

class LearnEngine:
    """Learns from multiple observation sessions across workers."""
    
    def __init__(self, db_path: str = "~/.osagnent/observations.db"):
        self.db_path = Path(db_path).expanduser()
        self.min_confidence = 0.95
        self.require_approval = True
    
    def batch_learn(self, worker_id: str, days: int = 7) -> list[dict]:
        """Learn from last N days of observations for a worker."""
        observations = here.recall(f"worker:{worker_id}", limit=1000)
        
        # Filter by time window
        cutoff = datetime.now() - timedelta(days=days)
        recent = [o for o in observations if o.get("timestamp", "") > cutoff.isoformat()]
        
        # Cluster by task type
        clusters = self._cluster_by_task(recent)
        
        # Score each cluster
        skills = []
        for cluster in clusters:
            confidence = self._score_confidence(cluster)
            skill = self._generate_skill_spec(cluster, confidence)
            skills.append(skill)
        
        return skills
    
    def _cluster_by_task(self, observations: list[dict]) -> list[list[dict]]:
        """Group observations by the task they represent."""
        clusters = {}
        for obs in observations:
            tool = obs.get("tool", "unknown")
            if tool not in clusters:
                clusters[tool] = []
            clusters[tool].append(obs)
        return list(clusters.values())
    
    def _score_confidence(self, cluster: list[dict]) -> float:
        """Score confidence that this is a real workflow."""
        if len(cluster) < 5:
            return 0.3
        if len(cluster) < 15:
            return 0.6
        if len(cluster) < 30:
            return 0.8
        return 0.95
    
    def _generate_skill_spec(self, cluster: list[dict], confidence: float) -> dict:
        """Generate a skill spec from a cluster of observations."""
        tool = cluster[0].get("tool", "unknown")
        args = [c.get("args", {}) for c in cluster[:10]]
        
        return {
            "name": f"learned_{tool}",
            "confidence": confidence,
            "trigger": f"when worker uses {tool}",
            "action": f"call {tool} with args from pattern",
            "args_pattern": self._extract_pattern(args),
            "requires_approval": confidence < 0.95,
            "sample_count": len(cluster),
        }
    
    def _extract_pattern(self, args_list: list[dict]) -> dict:
        """Extract the most common arg pattern."""
        if not args_list:
            return {}
        # Simple mode: use the first args as template
        return args_list[0] if args_list else {}
    
    def export_skill_specs(self, worker_id: str, output_dir: str = "~/.hermes/skills"):
        """Export learned skills to Hermes skills directory."""
        skills = self.batch_learn(worker_id)
        output = Path(output_dir).expanduser()
        
        for skill in skills:
            if skill["requires_approval"]:
                print(f"  ⏳ {skill['name']} — {skill['confidence']:.0%} confidence (pending approval)")
                here.remember(f"pending_skill:{skill['name']}", skill)
            else:
                self._write_skill(skill, output)
                print(f"  ✅ {skill['name']} — {skill['confidence']:.0%} confidence (deployed)")
    
    def _write_skill(self, skill: dict, output_dir: Path):
        """Write a skill file to the Hermes skills directory."""
        skill_name = skill["name"]
        skill_dir = output_dir / skill_name
        skill_dir.mkdir(exist_ok=True)
        
        # Write SKILL.md
        skill_md = f"""# {skill_name}

Auto-generated skill from OSagnent observation pipeline.
Confidence: {skill['confidence']:.0%}
Sample observations: {skill['sample_count']}

## When to Use
{skill['trigger']}

## What It Does
{skill['action']}

## Generated From
Learned from {skill['sample_count']} observations.
"""
        (skill_dir / "SKILL.md").write_text(skill_md)
        
        # Write config
        config = {
            "name": skill_name,
            "auto_generated": True,
            "confidence": skill["confidence"],
            "source": "osagnent_learn",
        }
        (skill_dir / "skill.json").write_text(json.dumps(config, indent=2))
