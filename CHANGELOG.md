# CHANGELOG

All notable changes to **Aurakl Forge** binaries published here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and this repository follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.6.0-rc1] — 2026-05-27

First public release candidate of Aurakl Forge — Phase 3 commercial-layer
gate validation. Bundles signed with minisign key `2853230EF41389B0`
(public key committed at [`minisign.pub`](./minisign.pub)).

### Highlights

- **Onboarding** — Forge desktop app first-run flow, device keypair
  registration to OS keychain.
- **Commercial layer** — RFC 8628 OAuth Device Authorization Grant
  against `crevo.aurakl.ai`, per-plan quota enforcement, 7-day
  SubscriptionGate cache with offline Hobby fallback.
- **LLM Gateway** — Aurakl-hosted Anthropic proxy with credit metering,
  switchable to local LLM or BYOK (Bring Your Own Key).
- **Updater** — Tauri updater plugin reads `latest.json` from this repo,
  verifies bundle signatures, and applies in-place updates.

### Known limitations

- macOS DMG is **not yet notarized** (Apple Developer Program enrollment
  pending). On first launch, macOS Gatekeeper will require explicit
  approval via **System Settings → Privacy & Security**.
- This is a release candidate — exercising the cross-repository
  release pipeline. Production-ready v0.6.0 will follow once notarization
  is wired up.
