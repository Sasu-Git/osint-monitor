#!/bin/sh
# ExecStartPre of osint-daemon.service: start only when the app checkout is exactly the pinned commit.
set -eu
pinned=$(tr -d '[:space:]' < /etc/osint/pinned_commit)
head=$(git -C /opt/osint/app rev-parse HEAD)
dirty=$(git -C /opt/osint/app status --porcelain --untracked-files=no)
if [ "${#pinned}" -lt 7 ] || [ "${head#"$pinned"}" = "$head" ]; then
  echo "refusing to start: /opt/osint/app is at $head, pinned is '$pinned'" >&2
  exit 1
fi
if [ -n "$dirty" ]; then
  echo "refusing to start: /opt/osint/app has local changes" >&2
  exit 1
fi
mkdir -p /opt/osint/app/data/logs
