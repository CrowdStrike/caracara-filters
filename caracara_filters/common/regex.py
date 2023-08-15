"""Caracara Filters: Shared Regular Expressions."""
import re


IP_ADDRESS_RE: re.Pattern[str] = re.compile(
    r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
)

RELATIVE_TIMESTAMP_RE: re.Pattern[str] = re.compile(
    r"^(?P<sign>[-+])(?P<number>\d+)(?P<scale>(s|m|h|d))$"
)
