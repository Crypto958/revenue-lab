# Local dev workflow — build here, serve from the VPS

Two machines, one site. This Mac builds; the Oracle VPS stays production.

```
  this Mac                                Oracle VPS (129.225.68.128)
  ────────                                ───────────────────────────
  ~/revenue-lab/  (git, source of truth)
       │
       │  ./deploy.sh urbania|westbridge|all
       ▼
                                      /home/ubuntu/revenue-lab/website/
                                        urbania/app/server.py  :8100  <─ cloudflared ─┐
                                        westbridge/            :8099  <─ cloudflared ─┤ public URL
                                                                                      ┘ (ephemeral trycloudflare)
```

## Daily loop

```bash
# 1. preview locally — the REAL app server, same code as production
cd ~/revenue-lab/website/urbania/app && PORT=8200 python3 server.py
#    -> http://127.0.0.1:8200/     (westbridge: python3 -m http.server 8200 in website/westbridge)

# 2. build / edit here ...

# 3. check nothing drifted while you worked
cd ~/revenue-lab && ./deploy.sh diff

# 4. ship it (add --dry-run first if unsure)
./deploy.sh urbania      # pushes app + restarts the :8100 server
./deploy.sh westbridge   # pushes static files, no restart needed
./deploy.sh all
```

`./deploy.sh status` shows what is actually running on the VPS.

## Two different site types

| Site | Type | Port | Deploy needs restart? |
|---|---|---|---|
| **urbania** | Python app (`app/server.py`, SQLite backend) | 8100 | **Yes** — `deploy.sh` handles it |
| **westbridge** | plain static HTML | 8099 | No — files are live on write |

Urbania's `server.py` also serves the static pages in `app/site/`, plus:
- `POST /api/trip` — accepts a trip request, returns a reference
- `GET  /api/trip/<REF>` — customer status lookup (no personal data)
- `GET  /admin` — owner pipeline board, gated by `ADMIN_TOKEN`
- `GET  /health` — liveness

## Hard rules (the deploy script enforces these)

1. **`data/` is never pushed.** It holds `trips.db` — real customer leads. Overwriting it destroys them.
2. **`.admin_token` is never pushed.** Secret.
3. **tar-over-ssh, not rsync.** macOS ships openrsync 2.6.9, which rejects the flags you'd want.

## Known fragility

- `/admin` is **currently disabled in production** — the running server has no `ADMIN_TOKEN`.
  A `.admin_token` file exists in `app/` but is unused. To enable: `./deploy.sh restart-urbania --with-admin`.
- The Urbania server's parent process is the **Hermes gateway**, not systemd. Nothing restarts it
  if it dies; a gateway restart or VM reboot takes the site down. Fix properly with a systemd unit.
- The public URL is a **cloudflared quick tunnel** — random subdomain, dies with the process.
  Not indexable as yours; needs a real domain + token for SEO.

## Paused on the VPS (so only this machine edits the site)

Resume with `hermes cron resume <id>` when a local build is finished:

| Job | ID |
|---|---|
| Revenue Lab — Chief heartbeat | `19e61cd5411e` |
| Revenue Lab — Morning Briefing | `88533a70fff0` |
| Revenue Lab — Outreach Engine (P1) | `ed139ded2782` |

## Syncing the other way (VPS -> here)

```bash
ssh -i ~/.ssh/oci_hermes ubuntu@129.225.68.128 \
  'tar czf - -C /home/ubuntu revenue-lab' | tar xzf - -C ~
```
