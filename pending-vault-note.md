# Pending canonical vault update: Agent Zero pilot deployed

## Verified completion update — 2026-10-21

Both pilots are live: http://<agent-zero-host>:50080 and http://<agent-zero-host>:50081. Native CA-derived Agent Zero v2.14 containers, Tailscale-only bindings, application authentication, separate persistent usr and Chromium profiles. Shared Bitwarden organization Airstream AI / collection Helix holds `Strix Agent Zero 1` and `Strix Agent Zero 2`; no passwords belong in Obsidian.

Main/utility inference uses existing local halogen-qwen3.8-flash-next on port8731. Bundled CPU embeddings verified offline. Real file/tool/browser tasks, two live XFCE desktop keyboard/pointer edits while active tasks were paused, resumed same-agent readback, independent activity while the other instance paused, native recreation persistence, and one bounded authenticated A2A exchange passed.

All17 original container IDs/states/start times preserved in the deployment continuation; qbit guard aligned; parity remains noncorrecting. No Plex/VPN/HA/array/backup changes. Autostart/templates/cache verified, not a host-reboot test.

Keep this a supervised pilot: model is text-only, not verified visual autonomy; reasoning can be slow and summaries can overclaim. An incorrect browser-restoration summary was caught and corrected using actual state-tool evidence. Evidence: `agent-zero-pilot/REPORT.md`, `acceptance-summary.json`, `final-infrastructure.json`, chat/tool logs, handoff screenshots and shared-vault item handles.

Canonical Obsidian has NOT been edited; this update remains pending canonical application. No sync claim.

## Superseded pre-maintenance history (retained for provenance)


Date: 2026-10-21. Suggested canonical note: Projects/Agent Zero pilot.md, linked from Projects index and Vault map. This file is pending application to the Mac canonical Obsidian vault; the VM reference vault was not edited and no sync is claimed.

Brian approved two isolated Agent Zero instances sharing local inference on Strix or DGX. Strix native Community Applications has an actual Agent Zero listing from Selfhosters; no custom-template exception is needed. Its upstream template needs documented local adaptations: no NVIDIA runtime on Strix, isolated `/a0/usr` persistence, private bindings, and secure authentication.

Attempted official image download on Strix failed at layer registration with `no space left on device`. Existing Docker image is 30 GiB at `/mnt/fastssd/system/docker/docker.img`. Fastssd has about 1.4 TiB free, but Docker storage is separately constrained. No agents were created and no existing services, disk assignments, parity settings, or credentials were changed. Partial image layers may be cached.

Decision needed: authorize native Docker image expansion, proposed 30 to 80 GiB, plus a planned Docker service maintenance window. Do not stop/restart the VPN, downloader, model server, or other workloads without explicit notice/approval. No automatic image prune.

Verified local basic inference on Strix endpoint port 8731 with model `halogen-qwen3.8-flash-next`; actual completion returned `LOCAL_READY`. Tool use, desktop control, and concurrent performance remain untested. Native noncorrecting parity check remains running. Bitwarden access recovery is also pending; no new credentials generated.

Evidence: `/home/helix/.hermes-minimal/workspace/agent-zero-pilot/REPORT.md`, `local-inference-probe.json`, `storage-blocker.txt`, `storage-inventory.txt`, `ca-search-result.json`, and `upstream-ca-template.xml`. Proposed ports 50080/50081 are not live.
