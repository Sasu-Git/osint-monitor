# Live daemon on a Linux host (Google Cloud VM)

Replaces the Windows supervisor, keep-awake and launcher (`scripts/ops/supervisor/`, `scripts/ops/keepawake/`) with
one systemd unit. The rules are the same:
- only the pinned commit starts;
- a stopped daemon is restarted;
- after 3 starts in an hour it stays down until a person looks.

A server does not sleep, so there is no keep-awake.

| | |
|---|---|
| Host | GCP project `osint-monitor-514209`, VM `osint-daemon`, `europe-north1-b`, e2-standard-2 (2 vCPU, 8 GB), Ubuntu 24.04. No inbound access from the internet; SSH only through IAP (`gcloud compute ssh osint-daemon --tunnel-through-iap`) |
| User | `osint` (system user, no login shell), home `/opt/osint` |
| Code | `/opt/osint/app`, detached at the approved commit (cloned from a git bundle: no GitHub credentials on the VM) |
| Python | 3.14.3 via `uv` (`/opt/osint/python`), venv `/opt/osint/venv`. Package versions identical to the laptop venv; torch is the CPU build (`torch==2.14.0+cpu`) |
| Models | spaCy `en_core_web_lg`, `it_core_news_md`, `es_core_news_md` 3.8.0; sentence-transformers `all-MiniLM-L6-v2` pinned at revision `1110a243`, loaded offline (`HF_HUB_OFFLINE=1`) |
| Database | `/opt/osint/data/live/window-2026-09-25.db` (set in `/etc/osint/daemon.env`) |
| Logs | `/opt/osint/app/data/logs/` (`daemon.err.log` and the rest, as on Windows); start/stop/exit codes in `journalctl -u osint-daemon` |
| Backups | disk snapshot schedule `osint-daily` (daily, 14 days, EU); database backups through the SQLite backup API as in the deployment runbook |

## Install (once)

The unit and `check_pin.sh` are installed outside the checkout, so they work whatever commit is checked out
(`$OPS` = a copy of this folder, e.g. from this branch's bundle):

```bash
sudo install -d -o root -g osint -m 0750 /etc/osint
sudo install -o root -g osint -m 0640 $OPS/daemon.env.example /etc/osint/daemon.env
git -C /opt/osint/app rev-parse HEAD | sudo tee /etc/osint/pinned_commit
sudo install -D -m 0755 $OPS/check_pin.sh /usr/local/lib/osint/check_pin.sh
sudo install -m 0644 $OPS/osint-daemon.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now osint-daemon
```

## Operating it

| Task | Command |
|---|---|
| State | `systemctl status osint-daemon`; `sudo -u osint env $(sudo cat /etc/osint/daemon.env) /opt/osint/venv/bin/python /opt/osint/app/main.py status` |
| Pause / resume collection (daemon stays up) | `main.py pause` / `main.py resume`, run as `osint` in `/opt/osint/app` |
| Deliberate stop (the Windows `HOLD`) | `sudo systemctl stop osint-daemon`. systemd does not restart a unit stopped this way. Pause first and let the running pipeline run finish, as in the runbook. |
| Start again | `sudo systemctl start osint-daemon` |
| After a crash loop | `sudo systemctl reset-failed osint-daemon`, after reading `daemon.err.log` |

## Deploying approved code

1. Copy a git bundle with the approved tag to the VM and run `git fetch` from it into `/opt/osint/app`.
2. Run the pre-deploy check and the verified backup from the deployment runbook with the target code.
3. `systemctl stop`, then `git checkout --detach <tag>`, then write the new SHA to `/etc/osint/pinned_commit`.
4. Run any migrations, then `systemctl start`.
5. Run the post-start checks (C1).

A start whose checkout is not the pinned commit, or has local changes, is refused by `check_pin.sh`.

**Rollback:** the same steps with the previous `production-stable-*` tag, and the runbook's database restore when the
candidate changed data.

## Dashboard and evaluations

The web server stays read-only. Either:
- run it on the VM and reach it through IAP port forwarding
  (`gcloud compute start-iap-tunnel osint-daemon 8790 --local-host-port=localhost:8790`); or
- keep it on the laptop over a backup-API snapshot pulled from the VM.

Evaluations always use snapshots.

## Equivalence with the laptop (rehearsal, 2026-11-09)

Same code `6d6e7c8`, same database snapshot (sha256 `662a4d46…`), laptop (Windows) vs VM (Linux):
- provenance and corroboration for 25 Developments: identical;
- entities for 300 items (1,110 entities across en, it and es): identical;
- embeddings: maximum difference 1.4e-7, floating point;
- clustering: 0 of 44,850 item pairs change side of the 0.45, 0.50 or 0.53 cosine cutoffs.
