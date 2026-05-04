"""Caracara Filters: Boolean Transform.

This file contains a function that coerces a boolean-like input (a Python bool or an
accepted string representation) into a Python bool.  The FQL serialisation layer
(``get_fql()``) is responsible for rendering ``True``/``False`` as the unquoted FQL
literals ``true``/``false``.

Use this transform for filters where the API's FQL field is a native boolean type
(e.g. ``is_lts:true``).  For filters that instead expect the string values ``'yes'``
or ``'no'``, use :func:`~caracara_filters.transforms.yes_no.yes_no_transform`.
"""

from typing import Union


def bool_transform(value: Union[str, bool]) -> bool:
    """Return a Python bool from a boolean or accepted string input."""
    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        return value.lower() in ["true", "yes"]

    raise ValueError(f"{str(value)} is not a boolean or a string")
