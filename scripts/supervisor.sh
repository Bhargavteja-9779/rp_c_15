#!/usr/bin/env bash
# Layer B supervisor: keeps restarting the agent CLI headlessly until state/agent_state.json says FINISHED.
# Usage: scripts/supervisor.sh            (foreground)   |  tmux new -d -s research-supervisor scripts/supervisor.sh
# Stop:  touch state/STOP   (or tmux kill-session -t research-supervisor)
set -u
cd "$(dirname "$0")/.."
mkdir -p logs
LOG=logs/supervisor.log
delays=(300 900 1800 3600)
i=0
detect_cli() {
  if command -v claude >/dev/null 2>&1; then echo "claude"; return; fi
  echo ""
}
CLI=$(detect_cli)
if [ -z "$CLI" ]; then
  echo "$(date -Is) no headless agent CLI found; paste BOOTSTRAP_PROMPT.txt manually" | tee -a "$LOG"; exit 1
fi
while true; do
  if grep -q '"status": "FINISHED"' state/agent_state.json 2>/dev/null; then echo "$(date -Is) FINISHED; supervisor exits" >> "$LOG"; exit 0; fi
  if [ -f state/STOP ]; then echo "$(date -Is) STOP file present; supervisor exits" >> "$LOG"; exit 0; fi
  echo "$(date -Is) starting agent ($CLI), attempt $i" >> "$LOG"
  out=$(mktemp)
  "$CLI" -p "$(cat BOOTSTRAP_PROMPT.txt)" --dangerously-skip-permissions >"$out" 2>&1
  rc=$?
  tail -n 40 "$out" >> "$LOG"; echo "$(date -Is) agent exited rc=$rc" >> "$LOG"
  # if the CLI reports a reset time, sleep until then; otherwise exponential backoff 5/15/30/60 min
  reset=$(grep -oiE 'reset[s]? (at|in) [^.]*' "$out" | head -1)
  rm -f "$out"
  if [ -n "$reset" ]; then echo "$(date -Is) limit message: $reset" >> "$LOG"; fi
  d=${delays[$(( i < 3 ? i : 3 ))]}
  echo "$(date -Is) sleeping ${d}s before restart" >> "$LOG"
  sleep "$d"; i=$((i+1))
done
