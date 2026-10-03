#!/usr/bin/env bash
# ============================================================================
# deploy.sh — local dev (this Mac)  ->  VPS production (Oracle Cloud)
#
# Shape: build here, push files back. The VPS keeps serving production; its
# Hermes cron loop is PAUSED so only this machine edits the site.
#
# HARD RULES
#   * NEVER pushes data/          -> that is live customer lead data (trips.db)
#   * NEVER pushes .admin_token   -> secret
#   * Uses tar-over-ssh, because macOS ships openrsync 2.6.9 (no usable flags)
#
# Usage:
#   ./deploy.sh status                 what is running on the VPS right now
#   ./deploy.sh diff                   what differs local vs production
#   ./deploy.sh urbania  [--dry-run]   push the Urbania app, then restart it
#   ./deploy.sh westbridge [--dry-run] push the static Westbridge site
#   ./deploy.sh all      [--dry-run]
#   ./deploy.sh restart-urbania        restart the app server, no file push
# ============================================================================
set -euo pipefail

VPS_HOST="ubuntu@129.225.68.128"
SSH_KEY="$HOME/.ssh/oci_hermes"
REMOTE_WEBSITE="/home/ubuntu/revenue-lab/website"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCAL_WEBSITE="$SCRIPT_DIR/website"

DRY_RUN=0
WITH_ADMIN=0
for a in "$@"; do
  case "$a" in
    --dry-run)    DRY_RUN=1 ;;
    --with-admin) WITH_ADMIN=1 ;;
  esac
done
CMD="${1:-status}"

# tar exclude patterns are matched against the paths inside the archive
EXCLUDES=(--exclude='./data' --exclude='./.admin_token' --exclude='./__pycache__'
          --exclude='./.DS_Store' --exclude='./_versions' --exclude='*.pyc'
          --exclude='./server.log')

ssh_run() { ssh -i "$SSH_KEY" -o BatchMode=yes -o ConnectTimeout=10 "$VPS_HOST" "$@"; }

hr() { printf '%s\n' "────────────────────────────────────────────────────────────"; }

# push_tree <local-relative-path> <remote-absolute-path> <label>
push_tree() {
  local rel="$1" remote="$2" label="$3"
  if [ ! -d "$LOCAL_WEBSITE/$rel" ]; then
    echo "ABORT: local path missing: $LOCAL_WEBSITE/$rel" >&2; exit 1
  fi
  hr
  echo "PUSH  $label"
  echo "  from  $LOCAL_WEBSITE/$rel"
  echo "  to    $VPS_HOST:$remote"
  echo "  skip  data/  .admin_token  __pycache__/_versions"
  if [ "$DRY_RUN" = 1 ]; then
    echo "  [dry-run] nothing sent."
    return 0
  fi
  ( cd "$LOCAL_WEBSITE/$rel" && tar czf - "${EXCLUDES[@]}" . ) \
    | ssh_run "mkdir -p '$remote' && tar xzf - -C '$remote'"
  echo "  pushed."
}

restart_urbania() {
  hr
  echo "RESTART Urbania app server (:8100)"
  if [ "$DRY_RUN" = 1 ]; then
    echo "  [dry-run] would pkill 'python3 server.py' and relaunch detached."
    echo "  admin board: $([ "$WITH_ADMIN" = 1 ] && echo 'ENABLED (--with-admin)' || echo 'left disabled (unchanged)')"
    return 0
  fi
  local admin_expr=""
  if [ "$WITH_ADMIN" = 1 ]; then
    # token is read on the VPS from the file; never crosses the wire or this shell
    admin_expr='ADMIN_TOKEN="$(cat .admin_token)"'
  fi
  ssh_run "
    set -e
    pkill -f 'python3 server.py' 2>/dev/null || true
    sleep 1
    cd '$REMOTE_WEBSITE/urbania/app'
    $admin_expr PORT=8100 setsid nohup python3 server.py > server.log 2>&1 < /dev/null &
    sleep 2
    echo -n '  health: '; curl -s -m 5 http://127.0.0.1:8100/health || echo 'NO RESPONSE'
    echo
  "
}

case "$CMD" in
  status)
    hr
    echo "PRODUCTION STATUS ($VPS_HOST)"
    ssh_run '
      for pid in $(pgrep -f "http.server|server.py"); do
        printf "  pid %-7s %-22s cwd=%s\n" "$pid" "$(ps -o comm= -p $pid)" "$(readlink /proc/$pid/cwd 2>/dev/null)"
      done
      echo -n "  urbania :8100 /health -> "; curl -s -m 4 http://127.0.0.1:8100/health || echo "DOWN"
      echo
      echo -n "  westbridge :8099 /     -> "; curl -s -o /dev/null -m 4 -w "%{http_code}\n" http://127.0.0.1:8099/ || echo "DOWN"
      echo -n "  tunnel 8100 alive      -> "; pgrep -f "cloudflared.*8100" >/dev/null && echo yes || echo NO
      echo -n "  tunnel 8099 alive      -> "; pgrep -f "cloudflared.*8099" >/dev/null && echo yes || echo NO
    '
    ;;
  diff)
    hr
    echo "DIFF local vs production (urbania/app)"
    ( cd "$LOCAL_WEBSITE/urbania/app" && find . -type f ! -path './data/*' ! -name '*.pyc' ! -name '.admin_token' ! -path './__pycache__/*' ! -name 'server.log' \
        | sort | xargs shasum -a 256 2>/dev/null | awk '{print $2"  "$1}' | sed 's|\./||' ) > /tmp/__local_app.sha
    ssh_run "cd '$REMOTE_WEBSITE/urbania/app' && find . -type f ! -path './data/*' ! -name '*.pyc' ! -name '.admin_token' ! -path './__pycache__/*' ! -name 'server.log' | sort | xargs sha256sum 2>/dev/null | awk '{print \$2\"  \"\$1}' | sed 's|\./||'" > /tmp/__remote_app.sha.raw
    if [ ! -s /tmp/__remote_app.sha.raw ]; then
      echo "  (could not hash remote side - sha256sum missing?)"
    else
      sort /tmp/__local_app.sha > /tmp/__l.sorted
      sort /tmp/__remote_app.sha.raw > /tmp/__r.sorted
      if diff -q /tmp/__l.sorted /tmp/__r.sorted >/dev/null; then
        echo "  IDENTICAL (no drift)"
      else
        echo "  DRIFT:"; diff /tmp/__l.sorted /tmp/__r.sorted | head -30
      fi
    fi
    ;;
  urbania)
    push_tree "urbania/app" "$REMOTE_WEBSITE/urbania/app" "Urbania app (site/ + server.py)"
    restart_urbania
    ;;
  westbridge)
    push_tree "westbridge" "$REMOTE_WEBSITE/westbridge" "Westbridge static site"
    ;;
  all)
    push_tree "urbania/app" "$REMOTE_WEBSITE/urbania/app" "Urbania app (site/ + server.py)"
    restart_urbania
    push_tree "westbridge" "$REMOTE_WEBSITE/westbridge" "Westbridge static site"
    ;;
  restart-urbania)
    restart_urbania
    ;;
  *)
    echo "unknown command: $CMD" >&2
    sed -n '9,22p' "${BASH_SOURCE[0]}"
    exit 1
    ;;
esac
