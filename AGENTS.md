# AGENTS.md

JSON log formatter for Graylog — distribution `entirius-py-graylog-json-formatter`, import `graylog_json_formatter`.

## Commands

| Command | Meaning |
|---|---|
| `make install` | sync dependencies (uv, incl. extras) |
| `make check` | lint + format-check (ruff) |
| `make fix` | auto-fix lint + format |
| `make test` | test suite (pytest) |

## Conventions

- English only: code, docs, commits, branches, PRs.
- MPL-2.0: every non-trivial source file carries the license header (pre-commit inserts it).
- Toolchain: uv + ruff + hatchling + pytest; all config in `pyproject.toml`; `uv.lock` committed.
- Git flow: `master` (production) + `develop` (integration); changes land via PR; semver tag on `master`.
- Never rename the import package `graylog_json_formatter` — it is a public API contract.
- Default: do not commit — git is the user's call.

## Architecture

Single class `GraylogJSONFormatter(logging.Formatter)` in `graylog_json_formatter/`: renders each
log record as JSON, forwards non-builtin `extra` attributes, and maps Python levels to Graylog
severities (`GRAYLOG_LEVEL`). No runtime dependencies.
