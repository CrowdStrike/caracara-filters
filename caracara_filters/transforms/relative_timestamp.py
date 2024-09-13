"""Caracara Filters: Relative Timestamp Transform.

This file contains the logic required to convert from a string (e.g., -30m) to an absolute
UTC ISO8601 timestamp. This is the format expected by the Falcon API, and enables filters
such as LastSeen.

Examples:
-1hr = take one hour away from the current time
-30m = take thirty mins away from the current time
-2d  = take 2 days away from the current time
+4d  = add 4 days to the current time
"""

import datetime

from caracara_filters.common import RELATIVE_TIMESTAMP_RE


def convert_relative_timestamp(original_timestamp: datetime, relative_timestamp: str) -> datetime:
    """Convert a relative timestamp into an absolute ISO8601 timestamp."""
    # Type of the below is Optional[re.Match[str]]; however, re.Match cannot be subscripted
    # on Python 3.7
    match = RELATIVE_TIMESTAMP_RE.match(relative_timestamp)
    if match is None:
        # This should be impossible, as we have the check function
        # above to make sure this ridiculous situation doesn't happen
        raise ValueError("The timestamp did not match the prescribed format")

    sign: str = match.group("sign")
    number = int(match.group("number"))
    scale: str = match.group("scale")

    # Convert to seconds to save code and effort
    if scale == "s":
        seconds = number
    elif scale == "m":
        seconds = number * 60
    elif scale == "h":
        seconds = number * 60 * 60
    elif scale == "d":
        seconds = number * 60 * 60 * 24
    else:
        # Assuming the regex did The Thing, this should be impossible
        raise ValueError("The relative timestamp did not contain a supported unit")

    if sign == "-":
        new_timestamp = original_timestamp - datetime.timedelta(seconds=seconds)
    else:
        new_timestamp = original_timestamp + datetime.timedelta(seconds=seconds)

    return new_timestamp


def relative_timestamp_transform(input_timestamp: str) -> str:
    """Convert a relative timestamp to an ISO8601 UTC timestamp for Falcon."""
    new_timestamp = convert_relative_timestamp(
        original_timestamp=datetime.datetime.now(tz=datetime.timezone.utc),
        relative_timestamp=input_timestamp,
    )
    formatted_timestamp: str = new_timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    return formatted_timestamp
