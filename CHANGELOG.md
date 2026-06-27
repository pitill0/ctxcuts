# Changelog

All notable changes to this project will be documented in this file.

This project follows a lightweight changelog format inspired by
[Keep a Changelog](https://keepachangelog.com/), without committing to strict
release automation yet.

## Unreleased

### Added

- Added `--root` / `-C` support to run commands against another project root.
- Initial documentation polish for the first public-facing iteration.
- Clearer explanation of reusable context gain in `ctxc stats`.
- Honest scope notes about what ctxcuts saves and what it does not promise.

## 0.1.0 - Planned

### Added

- `ctxc init` to create a local `.ctxcuts/` directory.
- `ctxc list` to show configured shortcuts.
- `ctxc expand` to expand shortcut invocations into focused prompts.
- `ctxc stats` to estimate shortcut input, expanded prompt size and reusable
  context portion.
- Default shortcut set:
  - `:r` review
  - `:f` fix
  - `:t` tests
  - `:d` docs
  - `:s` security
  - `:a` audit
  - `:q` quality
  - `:p` perf
  - `:x` explain
  - `:m` map
  - `:i` investigate
  - `:c` commit
- Example configuration in `examples/basic/.ctxcuts/`.
