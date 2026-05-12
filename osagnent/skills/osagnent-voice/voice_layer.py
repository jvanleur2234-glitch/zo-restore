"""
OSagnent Voice Layer
Bridges OpenAI Realtime API + Hermes Agent + Huly OS + Kill Switch
"""
import asyncio
import json
import os
import sys
from typing import Optional

# ── OpenAI Realtime API ──────────────────────────────────────
try:
    from openai import AsyncOpenAI
    client = AsyncOpenAI(api_key=os.environ["OPENAI_API_KEY"])
    REALTIME_AVAILABLE = True
except ImportError:
    client = None
    REALTIME_AVAILABLE = False
    print("pip install openai - openai>=1.0 for realtime voice", file=sys.stderr)

# ── Hermes Bridge ────────────────────────────────────────────
HERMES_URL = os.environ.get("OSAGNENT_KILL_SWITCH_URL", "http://localhost:5015")
WORKER_ID = os.environ.get("OSAGNENT_WORKER_ID", "jcpaid_001")
AGENT_ID = os.environ.get("OSAGNENT_AGENT_ID", "osagnent_voice_agent")

class OSagnentVoice:
    """Voice layer bridging realtime speech → Hermes thinking → Huly execution"""
    
    def __init__(self):
        self.hermes_proc: Optional[asyncio.subprocess.Process] = None
        self.session_id = f"osagnent-voice-{WORKER_ID}"
        self.turn_count = 0
        self.running = False
        
    async def start(self):
        """Boot the full stack"""
        print("[OSagnent] Booting voice layer...", flush=True)
        
        # 1. Start Hermes Agent in oneshot mode
        self.hermes_proc = await asyncio.create_subprocess_exec(
            "hermes", "chat", "-z",
            "--model", os.environ.get("HERMES_INFERENCE_MODEL", "nvidia/minimaxai/minimax-m2.7"),
            "--provider", os.environ.get("HERMES_INFERENCE_PROVIDER", "nvidia"),
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=os.environ.get("HERMES_HOME", "/root/.hermes/hermes-agent")
        )
        
        # 2. Register with Kill Switch
        import urllib.request
        try:
            req = urllib.request.Request(
                f"{HERMES_URL}/register",
                data=json.dumps({"worker_id": WORKER_ID, "agent_id": AGENT_ID}).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=5) as r:
                print(f"[OSagnent] Kill switch: {r.read().decode()}", flush=True)
        except Exception as e:
            print(f"[OSagnent] Kill switch registration failed (non-fatal): {e}", flush=True)
        
        self.running = True
        print("[OSagnent] Voice layer ready", flush=True)
        
    async def process_voice_input(self, audio_bytes: bytes) -> str:
        """Stream audio → Hermes → text response"""
        if not REALTIME_AVAILABLE or client is None:
            return "VOICE_LAYER_NOT_READY: OpenAI Realtime SDK not installed"
        
        self.turn_count += 1
        
        # Transcribe via OpenAI Realtime
        try:
            transcript = await client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=("audio.webm", audio_bytes, "audio/webm"),
                response_format="text"
            )
            user_text = transcript.text
        except Exception as e:
            return f"TRANSCRIPTION_ERROR: {e}"
        
        # Skip kill-switch check for voice (no response time for realtime)
        # But log the interaction
        try:
            import urllib.request
            req = urllib.request.Request(
                f"{HERMES_URL}/log",
                data=json.dumps({
                    "worker_id": WORKER_ID,
                    "agent_id": AGENT_ID,
                    "action": "voice_input",
                    "input": user_text,
                    "turn": self.turn_count
                }).encode(),
                headers={"Content-Type": "application/json"}
            )
            with urllib.request.urlopen(req, timeout=2):
                pass
        except Exception:
            pass
        
        # Send to Hermes Agent
        if self.hermes_proc and self.hermes_proc.stdin:
            msg = f"{user_text}\n"
            self.hermes_proc.stdin.write(msg.encode())
            await self.hermes_proc.stdin.drain()
            
            # Read response
            try:
                response_bytes = await asyncio.wait_for(
                    self.hermes_proc.stdout.readline(),
                    timeout=60
                )
                response = response_bytes.decode().strip()
            except asyncio.TimeoutError:
                response = "TIMEOUT: Hermes took too long"
            
            # Speak response (would use TTS here)
            return response
        
        return "NO_HERMES_SESSION"

    async def speak(self, text: str):
        """TTS via OpenAI"""
        if not REALTIME_AVAILABLE or client is None:
            return
        try:
            response = await client.audio.speech.create(
                model="gpt-4o-mini-tts",
                voice="ash",
                input=text,
                response_format="audioopus"
            )
            audio_data = response.read()
            # Would play via speaker here
            return audio_data
        except Exception as e:
            print(f"[OSagnent] TTS error: {e}", flush=True)

    async def shutdown(self):
        self.running = False
        if self.hermes_proc:
            self.hermes_proc.terminate()
            await self.hermes_proc.wait()

if __name__ == "__main__":
    layer = OSagnentVoice()
    print("OSagnent Voice Layer — type 'quit' to exit")
    asyncio.run(layer.start())
    print("[OSagnent] Voice layer started. (Full voice I/O requires OpenAI API key + realtime SDK)")
