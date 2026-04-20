"""Daily revenue check — runs once per day, logs Stripe payments."""
import os
from datetime import datetime, timedelta

HEARTBEAT_DIR = "/home/workspace/.agent/heartbeat"
REVENUE_FLAG = f"{HEARTBEAT_DIR}/.last_revenue_check"
REVENUE_LOG = "/home/workspace/solomon-vault/brain/revenue_log.md"

def run():
    try:
        if os.path.exists(REVENUE_FLAG):
            last = datetime.fromtimestamp(os.path.getmtime(REVENUE_FLAG))
            if datetime.now() - last < timedelta(days=1):
                return False, "Revenue check done today"
        
        # Check Stripe payments via API
        # Note: requires STRIPE_SECRET_KEY in env
        import subprocess
        result = subprocess.run(
            ["node", "-e", """
const https = require('https');
const apiKey = process.env.STRIPE_SECRET_KEY;
const auth = Buffer.from(apiKey + ':').toString('base64');
const req = https.request({
    hostname: 'api.stripe.com',
    path: '/v1/payment_intents?created[gte]=' + Math.floor((Date.now()-86400000)/1000),
    method: 'GET',
    headers: { 'Authorization': 'Basic ' + auth }
}, res => {
    let d = ''; res.on('data', c => d += c);
    res.on('end', () => {
        try {
            const r = JSON.parse(d);
            const total = (r.data || []).reduce((s, p) => s + (p.amount || 0), 0);
            console.log(JSON.stringify({ count: r.data?.length || 0, total_cents: total }));
        } catch(e) { console.log('{}'); }
    });
});
req.end();
            """],
            capture_output=True, text=True, timeout=10,
            cwd="/home/workspace",
            env={**os.environ}
        )
        data = {}
        try:
            data = __import__('json').loads(result.stdout.strip() or '{}')
        except:
            pass
        
        count = data.get('count', 0)
        total = data.get('total_cents', 0) / 100
        
        # Log it
        os.makedirs(os.path.dirname(REVENUE_LOG), exist_ok=True)
        with open(REVENUE_LOG, 'a') as f:
            f.write(f"\n## {datetime.now().strftime('%Y-%m-%d')} — ${total:.2f} ({count} payments)\n")
        
        open(REVENUE_FLAG, 'w').close()
        return True, f"Revenue: ${total:.2f} ({count} payments)"
    except Exception as e:
        return False, f"Revenue check failed: {e}"
