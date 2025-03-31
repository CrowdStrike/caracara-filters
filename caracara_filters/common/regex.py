"""Caracara Filters: Shared Regular Expressions."""

import re

IP_ADDRESS_RE = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

ISO8601_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
RELATIVE_TIMESTAMP_RE = re.compile(r"^(?P<sign>[-+])(?P<number>\d+)(?P<scale>(s|m|h|d))$")
