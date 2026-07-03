# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import json
import logging
from datetime import datetime

BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}

# python logging are not using more levels
# graylog level is based on syslog level
GRAYLOG_LEVEL = {
    logging.DEBUG: 7,
    logging.INFO: 6,
    # logging.INFO: 5, # should be Notice
    logging.WARNING: 4,
    logging.ERROR: 3,
    # logging.CRITICAL: 2, # should be Critical
    # logging.CRITICAL: 1, # should be Alert
    logging.CRITICAL: 0,  # should be Emergency
}


class GraylogJSONFormatter(logging.Formatter):
    """JSON log formatter prepared for graylog.

    Usage example::

        import logging

        import graylog_json_formatter

        json_handler = logging.FileHandler(filename='log/test.json.log')
        json_handler.setFormatter(graylog_json_formatter.GraylogJSONFormatter())

        logger = logging.getLogger('my_json')
        logger.addHandler(json_handler)

        logger.info('Order created', extra={'order_id': '18'})

    The log file will contain the following log record (inline)::

        {
            "message": "Order created",
            "datetime": "2022-08-08T14:58:26.524448",
            "order_id": "18",
            "level_name": "INFO",
            "level": 6,
            "channel": "test_graylog_json_formatter.test"
        }

    """

    json_lib = json

    def format(self, record):
        message = record.getMessage()
        extra = self.extra_from_record(record)
        json_record = self.json_record(message, extra, record)
        mutated_record = self.mutate_json_record(json_record)
        # Backwards compatibility: Functions that overwrite this but don't
        # return a new value will return None because they modified the
        # argument passed in.
        if mutated_record is None:
            mutated_record = json_record
        return self.to_json(mutated_record)

    def to_json(self, record):
        """Converts record dict to a JSON string.

        It makes best effort to serialize a record (represents an object as a string)
        instead of raising TypeError if json library supports default argument.
        Note, ujson doesn't support it.
        ValueError and OverflowError are also caught to avoid crashing an app,
        e.g., due to circular reference.

        Override this method to change the way dict is converted to JSON.

        """
        try:
            return self.json_lib.dumps(record, default=_json_serializable)
        # ujson doesn't support default argument and raises TypeError.
        # "ValueError: Circular reference detected" is raised
        # when there is a reference to object inside the object itself.
        except (TypeError, ValueError, OverflowError):
            try:
                return self.json_lib.dumps(record)
            except (TypeError, ValueError, OverflowError):
                return "{}"

    def extra_from_record(self, record):
        """Returns `extra` dict you passed to logger.

        The `extra` keyword argument is used to populate the `__dict__` of
        the `LogRecord`.

        """
        return {
            attr_name: record.__dict__[attr_name] for attr_name in record.__dict__ if attr_name not in BUILTIN_ATTRS
        }

    def json_record(self, message, extra, record):
        """Prepares a JSON payload which will be logged.

        Override this method to change JSON log format.

        :param message: Log message, e.g., `logger.info(msg='Order created')`.
        :param extra: Dictionary that was passed as `extra` param
            `logger.info('Order created', extra={'order_id': '18'})`.
        :param record: `LogRecord` we got from `JSONFormatter.format()`.
        :return: Dictionary which will be passed to JSON lib.

        """
        extra["message"] = message

        # Graylog uses timestamp field for his own purpose.
        # To setup log time, we are using pipelien to override datetime to timestamp.
        # On datetime you should use now() not utcnow().
        if "datetime" not in extra:
            extra["datetime"] = datetime.now()

        if record.exc_info:
            extra["exception"] = {
                "message": str(record.exc_info[1]),
                "class": str(record.exc_info[0]),
                "trace": self.formatException(record.exc_info),
            }

        extra["level_name"] = record.levelname
        extra["level"] = (
            GRAYLOG_LEVEL[record.levelno] if GRAYLOG_LEVEL[record.levelno] is not None else GRAYLOG_LEVEL[logging.INFO]
        )

        if "channel" not in extra:
            extra["channel"] = record.name

        if "function" not in extra:
            extra["function"] = record.funcName

        return extra

    def mutate_json_record(self, json_record):
        """Override it to convert fields of `json_record` to needed types.

        Default implementation converts `datetime` to string in ISO8601 format.

        """
        for attr_name in json_record:
            attr = json_record[attr_name]
            if isinstance(attr, datetime):
                json_record[attr_name] = attr.isoformat()
        return json_record


def _json_serializable(obj):
    try:
        return obj.__dict__
    except AttributeError:
        return str(obj)
