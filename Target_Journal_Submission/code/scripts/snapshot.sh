#!/usr/bin/env bash
# Nightly project snapshot (excludes raw data, checkpoints and submission zips); keeps the last 3 in backups/.
cd "$(dirname "$0")/.."; mkdir -p backups
tar --exclude=./data --exclude=./backups --exclude=./checkpoints --exclude=./.git --exclude='*.zip' --exclude=./quick_outputs -czf "backups/project_snapshot_$(date +%Y%m%d_%H%M).tar.gz" .
ls -1t backups/project_snapshot_*.tar.gz | tail -n +4 | xargs -r rm -f
