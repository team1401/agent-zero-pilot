# Agent Zero two-instance pilot — deployed and functionally verified

Verified 2026-10-21 on Strix. Both pilots are running, authenticated, native Unraid-managed, and idle after bounded tests. No original application was restarted during this deployment continuation.

## Access and credentials

- Instance 1: **http://<agent-zero-host>:50080** — `agent-zero-1`
- Instance 2: **http://<agent-zero-host>:50081** — `agent-zero-2`
- Access requires Tailscale and application login. Docker publishes only the Tailscale host IP, not 0.0.0.0, LAN IP, SSH, or desktop backend ports.
- Shared Bitwarden organization **Airstream AI**, collection **Helix**:
  - `Strix Agent Zero 1`: `4534c9ae-e837-420c-9ad0-b4ea0101619a`
  - `Strix Agent Zero 2`: `cad97de5-9b59-40d4-bc76-b4ea0101706c`
- Both items were created, moved to the shared collection, and read back to verify unchanged logins and exact organization/collection membership. No credential values appear in this report. Protected app-consumed copies remain in each persistent `usr/.env`; temporary local credential/session copies were removed after verification.
- The UI displays its generic HTTP warning. These URLs use encrypted Tailscale transport, not application-level HTTPS; do not publish them outside the tailnet.

## Installed configuration

- Official `agent0ai/agent-zero:latest`, actual image source **v2.14**, revision `ff2a5b9c9c4e490ba38dd7c313e779510bb2071a`.
- Pulled digest: `sha256:b0c9763df7b8c4c5ddbdac9c101e8f84de8b7cdf9185203e446e2d7d8ebf2f1c`.
- Derived from the actual Selfhosters CA listing/template. Retained repository, registry, project, support, TemplateURL and icon; removed optional NVIDIA runtime and stale whole-/a0 guidance.
- Native editable templates: `/boot/config/plugins/dockerMan/templates-user/my-agent-zero-{1,2}.xml`. Created/recreated through installed Docker Manager helpers. Native cache confirms running, autostart=true, correct WebUI/icon/template links.
- Persistent isolated mounts per instance:
  - `/mnt/fastssd/AppData/agent-zero-N/usr` → `/a0/usr`
  - `/mnt/fastssd/AppData/agent-zero-N/browser` → `/a0/tmp/browser`
- The extra browser mount is necessary because upstream v2.14 keeps Chromium profiles outside `/a0/usr`. Existing profiles were copied while only the new pilots were stopped, then both were recreated natively. Chats, handoff files, desktop startup and existing browser tab state were reverified afterward.
- Bridge networking; no privileged mode, Docker socket, host-root mount, host networking, GPU passthrough or public tunnel. Each pilot limited to 8 GiB RAM and four CPU equivalents; 1 GiB shared memory.
- Appdata/usr roots mode700; consumed `.env` mode600. Native shell entrypoint sets umask077 before official initialization. Verified `.env` remains600 after a real settings save (upstream otherwise rewrites it644).

## Local model compatibility

Both main and utility presets use:

- Provider adapter: `lm_studio` (OpenAI-compatible chat).
- Endpoint: `http://<agent-zero-host>:8731/v1`.
- Model: **`halogen-qwen3.8-flash-next`**.
- Context configured32768; output limit4096; temperature0.2; vision=false.
- Embeddings: bundled **sentence-transformers/all-MiniLM-L6-v2**, CPU. Both actual Agent Zero wrappers generated finite **384-dimensional** vectors with Hugging Face and Transformers forced offline. Offline flags are now persistent template environment values.

No cloud model credentials, cloud inference spend, GPU allocation or large model downloads were introduced. The official image contained the embedding model. Startup automatically fetched a small 12.2 MiB spaCy language package; that is not a new inference model installation.

## Actual acceptance tests

| Test | Result |
|---|---|
| Auth boundary | Both root and API redirect unauthenticated callers to login; desktop endpoint returns401. Correct stored credentials successfully authenticate. Rechecked after native recreation. |
| Agent tool execution | Each local-model agent created its own scratch file using `code_execution_tool`, then read it back. Actual tool outputs retained. |
| Agent browser | Each independently opened `https://example.com/`; actual browser tool returned title `Example Domain`. |
| Separate state | Each container lacked the other instance's scratch filename. Different host data roots, chats, processes and browser profiles. |
| Live desktop input | Both XFCE/Xpra desktops started; LibreOffice opened the agent-created files. Actual pointer and keyboard events through authenticated Xpra changed and saved them. This was not screenshot-only testing. |
| Pause/human/resume | A running task in each instance was paused, GUI edits saved, then resumed. The same agent read the changed file. Final markers: instance1 `humanhandoffonefinal`; instance2 `humanhandofftwo` (LibreOffice adds a UTF-8 BOM). |
| Independent activity | Instance2 completed its own tool/file verification while instance1's active task remained paused. |
| Persistence | Native container recreation preserved chats and handoff markers. Both desktops restarted. Actual `browser state` tool results confirmed existing tab1 with `https://example.com/` and `Example Domain` afterward. |
| A2A | Enabled with credential-derived token authentication. Invalid-token requests401, valid agent cards200 on both. One controlled request executed from instance1's container to instance2; task reached completed with actual local-model reply `A2A_LOCAL_OK`. No autonomous chatter configured. |
| Native management | Both native cache entries show running/autostart and correct links. Original autostart schedule preserved exactly as a prefix, with only two pilot entries appended. |

A2A current route uses secret token prefix, trailing-slash JSON-RPC endpoint and `/.well-known/agent.json`; token URLs are intentionally omitted. MCP server remains disabled. A2A task memory is runtime-local; the successful pre-recreation task evidence is retained, and post-recreation token/agent-card checks pass.

## Limitations found — do not oversell

- **Corrected by actual vision testing, 2026-10-21:** the initial `vision=false` preset was not evidence of a text-only backend. Live Halogen supports images; a direct randomized image test passed, and Agent Zero completed a two-stage screenshot-only coordinate navigation challenge after one bounded retry. Only the new test chat had vision enabled; global defaults remain unchanged. Initial four clicks missed due to incorrect visual coordinate estimates; retry completed in two clicks after native screenshot dimensions were clarified, without supplying target coordinates. See `../agent-zero-vision-test/verification.json` and `REPORT.md`. General GUI reliability is not established.
- Simple tasks can take minutes because this model sometimes reasons at length, especially with both instances active. No stress/concurrency capacity guarantee is made.
- During the recreation check, both agents initially claimed a browser tab was restored despite an empty lazy-runtime list result. That claim was rejected. A fresh `state` action subsequently returned real matching URL/title evidence. Tool output must remain the acceptance criterion, not the model's final prose.
- The operator initially used `detail` for tab metadata; it requires an element ref. Corrected to `state`. No source patch or fabricated result was used.
- Headless Xpra screenshot rendering briefly went blank/timed out; real desktop input still worked and independent server-side captures verified the saved GUI content. This is not a claim that every client/browser combination has been tested.
- No host reboot test was performed. Native autostart configuration and container-recreation persistence were verified, not a full boot cycle.

## Original workload and storage preservation

- All **17 original container IDs, states and start times** match the continuation baseline:15 running,2 stopped. No Plex/qBittorrent/VPN/HA/model-container lifecycle changes in this continuation.
- qbit dependency guard remains `aligned`; no disable marker or watchdog change introduced.
- Plex's prior autostart fix and proton-vpn60-second delay preserved with the exact original schedule.
- Native array remains STARTED; parity check remains noncorrecting (`mdResyncCorr=0`). No array, disk assignment, WD backup, parity or backup changes.
- Final Docker filesystem:80 GiB total,31 GiB used,50 GiB available (df rounded). Idle pilot memory approximately1.83 GiB each, under8 GiB caps.
- Earlier approved Docker-image maintenance is archived in `REPORT-before-deployment.md` and its maintenance artifacts; do not attribute that earlier service restart to this deployment continuation.

## Evidence / operational files

Primary evidence: `acceptance-summary.json`, `final-infrastructure.json`, `native-final.jsonl`, `final-chat-{1,2}.json`, `handoff-active-paused-1.json`, `handoff-active-before-resume-1.json`, `handoff-paused-2.json`, `handoff-during-{1,2}.json`, `independent-while-one-paused-2.json`, `browser-restore-final-{1,2}.json`, `embeddings-verification.json`, `a2a-verification.json`, `a2a-task-final.json`, `vault-shared-handles.jsonl`, and `desktop-handoff-{1,2}.png`.

Preparation/verification scripts and native XML are retained for reproducibility, not unattended rerun. They intentionally require private credentials for authenticated tests; local credential staging has been cleaned up. Canonical Obsidian has NOT been edited; `pending-vault-note.md` is a pending update only. Reusable workflow saved as skill `agent-zero-unraid-pilot`; secret-access skill updated for imported session ID mapping and shared-collection verification.
