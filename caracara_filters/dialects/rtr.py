"""Caracara Filters: RTR Dialect.

This module contains filters that are specific to the RTR API.
"""
from functools import partial
from typing import Any, Dict

from caracara_filters.dialects._base import default_filter
from caracara_filters.dialects._base import rebase_filters_on_default
from caracara_filters.validators import options_validator


RTR_COMMANDS = [
    "cat",
    "cd",
    "clear",
    "cp",
    "csrutil",
    "cswindiag",
    "encrypt",
    "env",
    "eventlog",
    "filehash",
    "get",
    "getsid",
    "history",
    "ifconfig",
    "ipconfig",
    "kill",
    "ls",
    "map",
    "memdump",
    "mkdir",
    "mount",
    "mv",
    "netstat",
    "ps",
    "put",
    "put-and-run",
    "reg",
    "restart",
    "rm",
    "run",
    "runscript",
    "shutdown",
    "tar",
    "umount",
    "unmap",
    "update",
    "users",
    "xmemdump",
    "zip",
]

rtr_base_command_filter = {
    "fql": "base_command",
    "validator": partial(options_validator, RTR_COMMANDS, case_sensitive=False),
    "help": "Filter RTR audit logs by base command.",
}

RTR_FILTERS: Dict[str, Dict[str, Any]] = {
    "basecommand": rtr_base_command_filter,
    "command": rtr_base_command_filter,
}

rebase_filters_on_default(default_filter, RTR_FILTERS)
