# entirius-py-graylog-json-formatter

A JSON log formatter for Graylog, part of Entirius, the open-source modular ecommerce platform. `GraylogJSONFormatter`
is a `logging.Formatter` that renders each record as one JSON object, passes `extra` fields through and maps Python
log levels to Graylog severities.

[![PyPI](https://img.shields.io/pypi/v/entirius-py-graylog-json-formatter.svg)](https://pypi.org/project/entirius-py-graylog-json-formatter/)
[![Python](https://img.shields.io/pypi/pyversions/entirius-py-graylog-json-formatter.svg)](https://pypi.org/project/entirius-py-graylog-json-formatter/)
[![License: MPL-2.0](https://img.shields.io/badge/license-MPL--2.0-blue.svg)](https://github.com/entirius/entirius-py-graylog-json-formatter/blob/develop/LICENSE)

## What it does

- Renders each log record as one JSON object with `message`, `datetime`, `level_name`, `level`, `channel` and
  `function`.
- Passes every `extra` field of the record through to the JSON output.
- Maps Python log levels to Graylog severity numbers.
- Adds the exception message, class and traceback when the record carries `exc_info`.

## Installation

```shell
uv add entirius-py-graylog-json-formatter
pip install entirius-py-graylog-json-formatter
```

The import name is `graylog_json_formatter`.

## Quick start

```python
import logging

from graylog_json_formatter import GraylogJSONFormatter

handler = logging.FileHandler(filename="app.json.log")
handler.setFormatter(GraylogJSONFormatter())
logger = logging.getLogger("my_json")
logger.addHandler(handler)
logger.info("Order created", extra={"order_id": "18"})
```

In Django `settings.py`, register it as a formatter:

```python
LOGGING["formatters"]["graylog_json"] = {"()": GraylogJSONFormatter}
LOGGING["handlers"]["graylog_file"] = {
    "class": "logging.FileHandler", "filename": "app.json.log", "formatter": "graylog_json",
}
```

## Requirements

- Python 3.11 or newer.
- No runtime dependencies.

## Documentation

- Entirius documentation: https://docs.entirius.com/
- Changelog: https://github.com/entirius/entirius-py-graylog-json-formatter/blob/develop/CHANGELOG.md

## Part of Entirius

This formatter is a dependency of the Entirius backend service (Volkanos).

- Backend service: https://github.com/entirius/entirius-service-volkanos
- Docker harness: https://github.com/entirius/entirius-zeno

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: https://github.com/entirius/entirius-py-graylog-json-formatter/blob/develop/AGENTS.md

## License

Mozilla Public License 2.0 (MPL-2.0) — see https://github.com/entirius/entirius-py-graylog-json-formatter/blob/develop/LICENSE.
