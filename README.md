# graylog-json-formatter

JSON log formatter for Graylog — a `logging.Formatter` that emits structured JSON,
passing record `extra` fields through and mapping Python log levels to Graylog severities.

## Installation

```shell
pip install entirius-py-graylog-json-formatter
```

## Usage

```python
import logging
import graylog_json_formatter

json_handler = logging.FileHandler(filename="app.json.log")
json_handler.setFormatter(graylog_json_formatter.GraylogJSONFormatter())

logger = logging.getLogger("my_json")
logger.addHandler(json_handler)

logger.info("Order created", extra={"order_id": "18"})
```

In Django `settings.py`:

```python
from graylog_json_formatter import GraylogJSONFormatter

LOGGING["formatters"]["graylog_json"] = {"()": GraylogJSONFormatter}
LOGGING["handlers"]["handler_name"] = {
    "level": "DEBUG",
    "class": "logging.FileHandler",
    "filename": os.path.join(LOG_DIR, "app.json.log"),
    "encoding": "utf8",
    "formatter": "graylog_json",
}
```

## Development

```shell
make install     # sync dependencies (uv)
make check       # lint + format check (ruff)
make test        # test suite (pytest)
```

Development and agent instructions: [AGENTS.md](AGENTS.md).

## License

Mozilla Public License 2.0 — see [LICENSE](LICENSE).
