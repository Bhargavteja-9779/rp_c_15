#!/usr/bin/env bash
# Install autostart for both layers on YOUR machine (Linux: cron @reboot; macOS: use launchd equivalently).
# Not installed in the cloud container this project was developed in, because that container is ephemeral.
set -e
cd "$(dirname "$0")/.."; P=$(pwd)
( crontab -l 2>/dev/null | grep -v "research-loop" ;
  echo "@reboot cd $P && tmux new -d -s research-compute 'python run_all.py --mode full --resume' # research-loop" ;
  echo "@reboot cd $P && tmux new -d -s research-supervisor scripts/supervisor.sh # research-loop" ;
  echo "*/20 * * * * cd $P && python scripts/watchdog.py # research-loop" ) | crontab -
echo "installed: crontab -l | grep research-loop"
