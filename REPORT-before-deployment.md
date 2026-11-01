# Agent Zero two-instance pilot — Docker capacity restored; deployment pending

## Approved maintenance checkpoint — 2026-10-21

- Expanded the EXISTING image from 30 to 80 GiB using native Docker Settings backend (`docker.cfg`, `emcmd cmdStatus=Apply`, installed `mount_image` enlargement). No image replacement, pruning, volume deletion, array stop, reboot, or WD changes.
- Confirmed actual image `/mnt/fastssd/system/docker/docker.img` resides on `/dev/nvme1n1p1`, btrfs fastssd, NOT systemssd. Backing available approximately 1.4 TiB before and after. Exact image length after: 85899345920 bytes. Mounted Docker filesystem: 80 GiB, 22 GiB used, 58 GiB free.
- Stop requested 15:13:00 UTC; native image unmounted 15:13:12; daemon back 15:13:16; originally running applications all started by 15:13:42. Later verification confirms 15/15 restored, all 17 existing IDs, restart policies and destination-sorted mounts unchanged; both previously stopped containers remain stopped.
- Private root-only remote backups: `/mnt/fastssd/system/agent-zero-maintenance-20261021-151300/` contains native configuration/template archive, autostart, full inspection inventories, and prior Docker log. Contains credentials: do not print/export indiscriminately.
- Dependency guard disabled only during maintenance via its supported `disabled` marker plus lock; restored absent marker and guard returns `aligned`. Port-sync untouched and ran successfully. qbit authenticated preferences/torrents HTTP 200 after login HTTP 204; zero torrents, tun0, listen_port=forwarded_port=40005. VPN healthy, same namespace as qbit; egress 149.40.62.115 and forwarded TCP reachable from Ubuntu. No namespace recreation required.
- Plex identity HTTP 200. Syncthing/Immich HTTP 200; Prowlarr/Tunarr/Sonarr/Radarr/Seerr expected redirects; OpenClaw healthy, HTTP 403 auth boundary; all Immich healthchecks healthy. Halogen models endpoint returns expected model. These are service restoration checks, not complete playback or AI-agent tests.
- Native cache refreshed. Pre-existing sonarr container lacks dockerman label; unchanged, not newly converted.
- Native docker_init removed Plex autostart due to PHP truthiness bug: `<TailscaleEnabled>false</TailscaleEnabled>` is treated as boolean true with host networking. Plex has no Tailscale env integration. Restored original autostart bytes and verified exact hash match. Template/backend unchanged; bug can recur on later native image mounts and deserves separate scoped fix.
- Array still STARTED, parity check still active noncorrecting (`mdResyncCorr=0`), progressing. No background pull/watch process left running by this checkpoint.
- Agent Zero image retry, credential provisioning and both actual UI/desktop/tool tests remain pending. Existing historical blocker details below are retained for provenance; capacity blocker is now resolved.
- Local scripts/evidence: `maintenance.php`, `verify-maintenance.php`, `maintenance-verification.txt`.

## Previous pre-maintenance report

Verification date: 2026-10-21. Target: Strix Unraid, 100.108.186.69 (LAN 192.168.1.40).

## Outcome / decision needed

The official image pull failed while registering a layer:

`write /opt/venv-a0/lib/python3.12/site-packages/triton/_C/libtriton.so: no space left on device`

No Agent Zero container or native user template was installed. No service was stopped/restarted, no image was deleted, no array/disk configuration was changed, and no credentials were created. Downloaded image layers may remain cached; `docker image inspect agent0ai/agent-zero:latest` confirms no complete image.

**Recommended next approval:** enlarge the existing Unraid Docker image from 30 GiB to 80 GiB through native Settings > Docker during an approved Docker-service maintenance window. The image is `/mnt/fastssd/system/docker/docker.img`; fastssd has approximately 1.4 TiB available. This would require stopping/restarting Docker workloads, including the VPN/downloader and model server, so it was NOT performed. Alternatively, approve removal of specifically reviewed unused images after dependency checks; no broad prune is proposed. Expanding capacity is preferable to consuming nearly all remaining headroom.

## Verified prerequisites

- Strix memory: 123 GiB total, 86 GiB available during preflight.
- Docker loop filesystem: 30 GiB; after failed pull 22 GiB used / 7.8 GiB available. Docker reports 20.4 GB of images and 6.952 GB reclaimable; reclaimable is not authorization to delete.
- Native Community Applications listing DOES exist: `agent-zero`, Selfhosters Unraid Discord Repository. Present in installed CA cache and public feed dated 2026-10-20 12:43.
- Template provenance: https://raw.githubusercontent.com/selfhosters/unRAID-CA-templates/master/templates/agent_zero.xml
- Image: `agent0ai/agent-zero:latest`, registry-reported digest `sha256:b0c9763df7b8c4c5ddbdac9c101e8f84de8b7cdf9185203e446e2d7d8ebf2f1c`; compressed full_size 3145720871 bytes. Image download failed; no runnable version verified. GitHub latest release reported v2.14; that does NOT prove the Docker tag contains v2.14.
- Inspected upstream source revision `ff2a5b9c9c4e490ba38dd7c313e779510bb2071a`, including installation, desktop, A2A, Docker entrypoint, model configuration, and auth source. No repository script executed.
- Existing local model endpoint: `http://100.108.186.69:8731/v1`, model ID `halogen-qwen3.8-flash-next`. Actual chat completion returned `LOCAL_READY`. This verifies basic generation, NOT Agent Zero tool/browser/vision compatibility or concurrent-agent performance.
- No Ollama or LM Studio container observed. Existing Halogen serving container was not changed. No model downloaded.
- Spark dev3 is online at 100.87.41.76; direct SSH was blocked by missing trusted host-key association. Did not bypass verification or change known_hosts; did not establish its current model inventory.
- qBittorrent remains running; proton-vpn remains healthy. Native parity check remains active with `mdResyncCorr=0`; no parity operation changed.

## Prepared deployment design (NOT installed)

- Names: `agent-zero-1`, `agent-zero-2`, both derived from the actual CA template and deployed via native Docker Manager, retaining Repository/Registry/Support/Project/Icon/TemplateURL.
- Proposed WebUI: `http://100.108.186.69:50080` and `http://100.108.186.69:50081`. Ports were free at preflight; recheck before installation. Bind Tailscale IP only by default, not 0.0.0.0 or public interfaces. LAN bindings, if desired, can be explicit to 192.168.1.40.
- Isolated persistent mounts: `/mnt/fastssd/AppData/agent-zero-1/usr:/a0/usr` and `/mnt/fastssd/AppData/agent-zero-2/usr:/a0/usr`. Current official installation docs recommend `/a0/usr`; the CA template and compose example still mount all `/a0`.
- Remove CA's optional NVIDIA runtime/device variable and Nvidia-plugin dependency: Strix does not need GPU passthrough for a remote/shared model API. Remove obsolete `--BRANCH=main` PostArgs; inspect actual pulled image startup contract before native creation.
- No privileged mode, Docker socket, host-root mounts, host networking, public tunnel, GPU capabilities, or SSH port publication.
- Chat and utility models should use a supported OpenAI-compatible provider pointed exclusively at the verified Halogen endpoint. Use bundled CPU HuggingFace embeddings; inspect actual image model-preset schema before writing. Current v2 source stores presets under `usr/plugins/_model_config/presets.yaml`; do not assume old settings keys still select models.
- Set unique UI authentication before publishing either instance. Upstream uses `AUTH_LOGIN`/`AUTH_PASSWORD` and `usr/.env`; durable credential source should be Bitwarden, with only an app-consumed protected copy on Strix. Mac Bitwarden exists but is locked; Keychain secret lookup failed. The documented historical source was located privately but did not match conservative explicit-password parsing, so no guess/unlock was attempted. This credential-access prerequisite remains unresolved. No secret values were output or copied.
- A2A is supported and token-authenticated at `/a2a/t-<token>`; token changes with credentials. Enable only after UI authentication and unauthorized-access tests, keep token URLs out of reports/logs, and use private networking. Leave disabled until tested.

## Still required after storage approval

Image pull and actual image-version/source verification; secure credential provisioning; native templates/create/start/autostart/cache verification; exact model preset readback; authenticated UI and unauthorized-access checks; real local tool/file/browser tasks; two independent desktop keyboard/mouse handoffs and pause/resume tests; screenshot evidence; independent sessions while one is paused; local-only inference routing checks; authenticated A2A exchange if feasible. No claim that agents are working yet.

## Evidence and files

All local task artifacts are in `workspace/agent-zero-pilot/`: upstream CA XML, CA cache/feed and search results, upstream source/doc snapshots, release/tag metadata, local-inference-probe.json, storage-blocker.txt, storage-inventory.txt, this report, and pending-vault-note.md. No remote user configuration backup was necessary because no remote configuration was modified. These downloaded public sources are references, not a fork or executed project.
