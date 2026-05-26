# Aurakl Forge Releases

**Release-only repository for [Aurakl Forge](https://crevo.aurakl.ai)** — a cross-platform desktop AI Agent Studio.

This repository contains only release artifacts; the source code is private. Use this repo to:

- Download official binaries (macOS / Linux / Windows)
- Read the [CHANGELOG](./CHANGELOG.md)
- Verify SHA256 checksums and minisign signatures
- Check the Tauri updater feed at `latest.json`

## Downloads

Visit [crevo.aurakl.ai/download](https://crevo.aurakl.ai/download) for platform-detected one-click installers, or browse releases below.

| Platform | Asset |
|---|---|
| macOS Apple Silicon | `forge_${VERSION}_aarch64.dmg` |
| macOS Intel | `forge_${VERSION}_x64.dmg` |
| Linux x86_64 | `forge_${VERSION}_amd64.AppImage` |
| Windows x86_64 | `forge_${VERSION}_x64-setup.exe` |

Each release also publishes `latest.json` consumed by the in-app **Settings → About → Check for Updates** feature (Tauri updater plugin).

## Signing & verification

All bundles are signed with minisign. The public verification key is committed at [`minisign.pub`](./minisign.pub).

```bash
minisign -Vm forge_0.6.0_aarch64.dmg -p minisign.pub
```

## License

See [LICENSE](./LICENSE).

## Issues & contributions

Source code is closed. Report bugs through the in-app feedback channel or email **support@aurakl.ai**.
