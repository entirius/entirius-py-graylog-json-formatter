# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging

from graylog_json_formatter import GraylogJSONFormatter


def test(tmp_path):
    json_handler = logging.FileHandler(filename=tmp_path / "test.json.log")
    json_handler.setFormatter(GraylogJSONFormatter())

    logger = logging.getLogger()
    logger.addHandler(json_handler)
    logger.setLevel(logging.DEBUG)

    logger.debug("Debug test")
    logger.info("Info test, Order created", extra={"order_id": "18"})
    logger.warning("Warning test")
    logger.error("Error test")
    logger.critical("Crit test")

    assert True
