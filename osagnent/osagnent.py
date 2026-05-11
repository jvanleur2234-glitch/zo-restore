#!/usr/bin/env python3
"""
OSagnent CLI — The AI-Native Operating System
Phase 2: Auto-Learn Pipeline

Usage:
  osagnent.py start <worker_id>   Start observing a worker
  osagnent.py stop                 Stop observing + generate skills
  osagnent.py status               Show learning status
  osagnent.py list                 List generated skills
  osagnent.py approve <skill>      Approve a pending skill
  osagnent.py correct <skill>      Record a correction
  osagnent.py dashboard            Open web dashboard
"""
import sys
import json
from pathlib import Path
from datetime import datetime

HERE_API = "http://localhost:5015"  # Kill Switch API

def cmd_start(worker_id: str):
    """Start observing a worker."""
    import urllib.request
    try:
        req = urllib.request.urlopen(f"{HERE_API}/workers/{worker_id}/start", timeout=5)
        print(f"✅ Started observing worker: {worker_id}")
        print(f"📊 Dashboard: https://josephv.zo.space/osagnent")
    except Exception as e:
        print(f"❌ Could not reach HERE API: {e}")
        print(f"   Start Hermes first: hermes chat -q 'start osagnent observe'")

def cmd_stop():
    """Stop observing and run batch learning."""
    from observe.auto_export import AutoExport
    from core.learn import LearnEngine
    from generate.skill_generator import SkillGenerator
    
    print("🛑 Stopping observation...")
    print("🧠 Running batch learning...")
    
    learn = LearnEngine()
    worker_id = "current"  # Would come from active session
    
    print(f"\n📚 Generating skills for {worker_id}...")
    learn.export_skill_specs(worker_id)
    
    gen = SkillGenerator()
    skills = gen.list_generated_skills()
    print(f"\n✅ Generated {len(skills)} skills:")
    for s in skills:
        status = "🔒 approved" if s["confidence"] >= 0.95 else "⏳ pending"
        print(f"  {status} {s['name']} ({s['confidence']:.0%})")

def cmd_status():
    """Show current learning status."""
    import urllib.request
    try:
        req = urllib.request.urlopen(f"{HERE_API}/status", timeout=5)
        data = json.loads(req.read())
        print("📊 OSagnent Status")
        print("=" * 40)
        for worker in data.get("workers", []):
            print(f"\n👤 Worker: {worker['id']}")
            print(f"   Observed: {worker.get('tool_calls', 0)} tool calls")
            print(f"   Patterns: {worker.get('patterns', 0)} found")
            print(f"   Skills:   {worker.get('skills', 0)} generated")
    except Exception as e:
        print(f"❌ HERE API offline: {e}")
        print(f"   Start Hermes to connect to HERE API")

def cmd_list():
    """List all generated skills."""
    from generate.skill_generator import SkillGenerator
    gen = SkillGenerator()
    skills = gen.list_generated_skills()
    if not skills:
        print("No skills generated yet.")
        print("Run: osagnent.py start <worker> → work → osagnent.py stop")
        return
    print(f"📚 OSagnent Skills ({len(skills)} total)")
    print("=" * 40)
    for s in skills:
        trust = s.get("confidence", 0.8)
        bar = "█" * int(trust * 10) + "░" * (10 - int(trust * 10))
        status = "✅" if trust >= 0.95 else "⚠️" if trust >= 0.7 else "❌"
        print(f"{status} [{bar}] {s['name']} ({trust:.0%})")

def cmd_approve(skill_name: str):
    """Approve a pending skill."""
    from generate.skill_generator import SkillGenerator
    gen = SkillGenerator()
    skills = {s["name"]: s for s in gen.list_generated_skills()}
    if skill_name not in skills:
        print(f"❌ Skill not found: {skill_name}")
        return
    skill = skills[skill_name]
    skill["approved"] = True
    skill["approved_at"] = datetime.now().isoformat()
    gen.generate(skill)
    print(f"✅ Approved: {skill_name}")

def cmd_correct(skill_name: str):
    """Record a correction for a skill."""
    from core.self_improve import SelfImprove
    improve = SelfImprove()
    print(f"Recording correction for: {skill_name}")
    print("(In production, this would capture the actual worker action)")
    improve.record_correction(skill_name, {"manual": True}, {"ai": "guessed"})
    print(f"✅ Correction recorded for {skill_name}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "start" and len(sys.argv) >= 3:
        cmd_start(sys.argv[2])
    elif cmd == "stop":
        cmd_stop()
    elif cmd == "status":
        cmd_status()
    elif cmd == "list":
        cmd_list()
    elif cmd == "approve" and len(sys.argv) >= 3:
        cmd_approve(sys.argv[2])
    elif cmd == "correct" and len(sys.argv) >= 3:
        cmd_correct(sys.argv[2])
    else:
        print(__doc__)
