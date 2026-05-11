"""Self-improvement loop for OSagnent skills."""
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

class SelfImprove:
    """Refines skills based on corrections and feedback."""
    
    def __init__(self, skills_dir: str = "~/.hermes/skills"):
        self.skills_dir = Path(skills_dir).expanduser()
        self.corrections = []
    
    def record_correction(self, skill_name: str, worker_action: dict, ai_action: dict):
        """Record when worker overrides AI's action."""
        correction = {
            "skill": skill_name,
            "worker_action": worker_action,
            "ai_action": ai_action,
            "timestamp": datetime.now().isoformat(),
        }
        self.corrections.append(correction)
        
        # Learn from correction
        self._update_skill(skill_name, correction)
    
    def _update_skill(self, skill_name: str, correction: dict):
        """Update skill based on correction."""
        skill_dir = self.skills_dir / skill_name
        if not skill_dir.exists():
            return
        
        # Update metadata
        meta_file = skill_dir / "osagnent_meta.json"
        if meta_file.exists():
            meta = json.loads(meta_file.read_text())
        else:
            meta = {"name": skill_name, "corrections": [], "confidence": 0.8}
        
        meta["corrections"] = meta.get("corrections", []) + [correction]
        meta["correction_count"] = len(meta["corrections"])
        meta["last_corrected"] = correction["timestamp"]
        meta["timestamp"] = datetime.now().isoformat()
        
        # If corrected 3+ times, lower confidence
        if meta["correction_count"] >= 3:
            meta["confidence"] = max(0.5, meta.get("confidence", 0.8) - 0.1)
        
        # If no corrections in 30 days, raise confidence slightly
        if meta.get("last_corrected"):
            last = datetime.fromisoformat(meta["last_corrected"])
            if (datetime.now() - last).days > 30:
                meta["confidence"] = min(0.99, meta.get("confidence", 0.8) + 0.02)
        
        meta_file.write_text(json.dumps(meta, indent=2))
        
        # Update SKILL.md notes
        skill_file = skill_dir / "SKILL.md"
        if skill_file.exists():
            content = skill_file.read_text()
            if "⚠️ CORRECTIONS MADE" not in content:
                content += f"\n\n## ⚠️ Corrections Made: {meta['correction_count']}\n"
                content += "This skill has been refined based on worker corrections.\n"
            skill_file.write_text(content)
    
    def get_trust_score(self, skill_name: str) -> float:
        """Get trust score for a skill (1.0 = fully trusted)."""
        meta_file = self.skills_dir / skill_name / "osagnent_meta.json"
        if not meta_file.exists():
            return 0.8  # Default
        
        meta = json.loads(meta_file.read_text())
        confidence = meta.get("confidence", 0.8)
        correction_count = meta.get("correction_count", 0)
        
        # Reduce trust for recently corrected skills
        if meta.get("last_corrected"):
            days_since = (datetime.now() - datetime.fromisoformat(meta["last_corrected"])).days
            if days_since < 7:
                confidence *= 0.8  # 20% discount for recent correction
        
        return confidence
    
    def suggest_skills_to_disable(self) -> list[str]:
        """Return skills that should be disabled due to low trust."""
        to_disable = []
        for skill_dir in self.skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            meta_file = skill_dir / "osagnent_meta.json"
            if not meta_file.exists():
                continue
            meta = json.loads(meta_file.read_text())
            if meta.get("confidence", 1.0) < 0.5:
                to_disable.append(skill_dir.name)
        return to_disable
