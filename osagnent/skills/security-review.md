---
name: security-review
description: Use when a PR is ready and needs a security check before founder approval, or when the weekly supply chain assessment is due
version: 1.0.0
tags: [security, owasp, review, supply-chain]
---

## Overview

Two modes: PR review (every PR) and supply chain assessment (weekly). Blocks merges on critical findings.

## PR review

Run in order. Stop and block if Critical found.

**1. Secret scan:**
```bash
git diff main...HEAD | grep -iE "(api_key|secret|password|token|private_key|SERVICE_KEY|DATABASE_URL)\s*=" | grep -v "your-" | grep -v "example"
git ls-files | grep -iE "\.env"
```

**2. Dangerous patterns — flag any:**
- `eval(` in non-test code
- SQL built by string concatenation
- `dangerouslySetInnerHTML` without sanitization
- Supabase `service_role` key referenced client-side

**3. CVE check — only if `package.json` or `requirements.txt` changed:**
```bash
npm audit --audit-level=high
pip-audit --severity high
```

**4. OWASP check in diff:**
- Routes that mutate data but skip auth middleware
- User input passed directly to queries (injection risk)
- Secrets or PII in `console.log` / logger calls
- New Supabase tables without RLS enabled

**5. Post findings as PR comment:**
```bash
gh pr comment [number] --body "[security findings or 'Security: clean']"
```

**6. Severity action:**

| Finding | Action |
|---|---|
| Critical | `hermes kanban block [id]` + alert founder via gateway immediately |
| High | Block card + PR comment with specific fix for Dev Agent |
| Medium | PR comment only — fix before next sprint, does not block |
| Clean | Hand off to `await-merge-approval` |

## Supply chain assessment (weekly)

1. `npm audit --audit-level=moderate` or `pip-audit`
2. List direct deps and flag: publisher changed in last 30 days, name is a near-match of a popular package
3. Send plain-English summary to founder — packages checked, flags found, action needed

## OWASP clean code rules

Flag any of these in generated or reviewed code:

| OWASP | Bad pattern | Required |
|---|---|---|
| A01 Access Control | Unprotected mutation routes | Auth required on all write endpoints |
| A02 Crypto | MD5/SHA1 for passwords, plaintext secrets | bcrypt/argon2, secrets in env only |
| A03 Injection | String-concatenated queries | Parameterized queries only |
| A05 Misconfiguration | `service_role` key client-side | Anon key client-side, service key server-only |
| A07 Auth | No session expiry | Expiry set, tokens not stored in localStorage |
| A09 Logging | `console.log(secret)` | Never log credentials or PII |

## Verification

- PR has a security comment (clean or findings listed)
- Critical/High findings blocked the kanban card
- Founder notified if merge blocked
