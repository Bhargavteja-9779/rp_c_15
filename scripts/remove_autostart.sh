#!/usr/bin/env bash
crontab -l 2>/dev/null | grep -v "research-loop" | crontab - ; echo "autostart removed"
