"""
OSagnent Cua Plugin — observe then act
Holds cua session info, tracks actions, logs to /tmp/osagnent-actions.log
"""

import os, time, json
from datetime import datetime

LOG_FILE = "/tmp/osagnent-actions.log"
SESSION_FILE = "/tmp/osagnent-cua-session.json"

def log(msg):
    ts = datetime.now().isoformat()
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")
    except:
        pass

def hook_pre_tool(tool_name, tool_input, agent_id):
    """Called before each tool. Track what agent wants to do."""
    session = {
        "agent_id": agent_id,
        "tool": tool_name,
        "input": str(tool_input)[:200],
        "ts": datetime.now().isoformat()
    }
    try:
        with open(SESSION_FILE, "w") as f:
            json.dump(session, f)
    except:
        pass
    log(f"PRE {agent_id} -> {tool_name}")
    return {"allow": True}

def hook_post_tool(tool_name, tool_output, agent_id):
    """Called after each tool. Log the result."""
    log(f"POST {agent_id} <- {tool_name}: {'ok' if tool_output else 'fail'}")
    return {"continue": True}

def hook_start(agent_id):
    log(f"AGENT START {agent_id}")
    os.environ["OSAGNENT_CUA_ACTIVE"] = "1"

def hook_end(agent_id):
    log(f"AGENT END {agent_id}")
    os.environ.pop("OSAGNENT_CUA_ACTIVE", None)

def get_status():
    """Return current cua session status."""
    try:
        with open(SESSION_FILE) as f:
            return json.load(f)
    except:
        pass
    return {"status": "idle", "agent_id": None}
