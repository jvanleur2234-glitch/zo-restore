"""Check job queue and trigger job runner if pending jobs exist."""
import os

JOB_PENDING = "/home/workspace/.agent/jobs/pending"

def run():
    try:
        pending = os.listdir(JOB_PENDING)
        if pending:
            msg = f"{len(pending)} jobs pending: {', '.join(pending[:5])}"
            # Job runner daemon handles execution — just log it
            return True, msg
        return False, "Job queue empty"
    except Exception as e:
        return False, f"Job queue check failed: {e}"
