"""Caracara Filters: FQL Class.

This file contains a class that can be instantiated to contain filters. It must be configured with
a dialect, after which filters can be added.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Type, Union
from uuid import uuid4

from caracara_filters.common import FILTER_OPERATORS
from caracara_filters.dialects import DIALECTS


@dataclass
class FilterArgs:
    """Generic dataclass to hold a filter and its validated/transformed arguments.

    The contents of this dataclass are used once get_fql() is called. By storing the resultant
    data here, we can avoid needing to re-run any transformation of validation functions at the
    time that we actually require the FQL string.
    """

    filter_def: str
    fql: str
    value: Any
    operator: str


class FQLGenerator:
    """Caracara FQL Generator Class.

    This class will configure itself based on the chosen dialect (base, hosts, etc.), and will
    expose a very similar interface to its predecessor, Caracara's FalconFilter.

    When a filter is created, it will be validated and its inputs values transformed before being
    stored into the object. This means that changing a filter value once it has been stored is not
    supported, as the transforms and validators will be bypassed.
    """

    def __init__(self, dialect: str = "base"):
        """Create a new FQL generator with a specific dialect."""
        if dialect not in DIALECTS:
            raise ValueError(
                f"The specified dialect does not exist. Valid choices are: {str(DIALECTS.keys())}."
            )

        if dialect == "base":
            self.available_filters: Dict[str, Dict[str, Any]] = DIALECTS["base"]
        else:
            self.available_filters: Dict[str, Dict[str, Any]] = {
                **DIALECTS["base"],
                **DIALECTS[dialect],
            }

        self.dialect: str = dialect
        self.filters: Dict[str, FilterArgs] = {}

    def _validate_input_type(
        self,
        filter_name: str,
        filter_def: Dict[str, Any],
        value: Any,
    ) -> None:
        """Validate the data type of a filter's input, based on the filter definition."""
        data_types: List[Type] = filter_def["data_types"]
        multivariate: bool = filter_def["multivariate"]
        nullable: bool = filter_def["nullable"]

        if isinstance(value, list):
            if (
                multivariate is True
                and value
                and not any(isinstance(value[0], x) for x in data_types)
            ):
                raise TypeError(
                    "You provided a list for %s, but the type of the first item (%s) was not in "
                    "the list of acceptable types (%s)",
                    filter_name,
                    str(type(value)),
                    ", ".join(str(type(x)) for x in data_types),
                )
            if multivariate is False:
                raise TypeError(
                    f"The filter {filter_name} is not multivariate, but you provided a list."
                )
        elif value is None and not nullable:
            raise TypeError(
                f"The filter {filter_name} is not nullable, but you provided a NoneType."
            )
        elif value is None and nullable:
            # This is okay
            pass
        else:
            if not any(isinstance(value, x) for x in data_types):
                raise TypeError(
                    "The type of the filter %s (%s) was not in the list of acceptable types (%s)",
                    filter_name,
                    str(type(value)),
                    ", ".join(str(type(x)) for x in data_types),
                )

    def _validate_and_transform(
        self,
        filter_name: str,
        filter_def: Dict[str, Any],
        value: Any,
    ) -> Union[List[Any], str]:
        """Take an input from a developer or user and return a valid filter value."""
        multivariate: bool = filter_def["multivariate"]
        transform_func: Callable[[Any], Any] = filter_def["transform"]
        validation_func: Callable[[Any], bool] = filter_def["validator"]

        # Handle multivariate options by validating and transforming each option individually
        if multivariate and isinstance(value, list):
            transformed_value = []
            for val in value:
                # Validate the input
                if not validation_func(val):
                    raise ValueError(f"The input {val} is not valid for filter type {filter}.")

                # Transform the input
                transformed_val = transform_func(val)

                # Replace the value in the list
                transformed_value.append(transformed_val)

        else:
            # Non-multivariate input, so just handle the items directly
            # Run through the validation function
            if not validation_func(value):
                raise ValueError(f"The input {value} is not valid for filter type {filter_name}.")

            # Transform the input
            transformed_value = transform_func(value)

        return transformed_value

    def add_filter(self, new_filter: FilterArgs) -> str:
        """Add a new filter to the FQLGenerator object."""
        filter_id = str(uuid4())
        self.filters[filter_id] = new_filter
        return filter_id

    def remove_filter(self, filter_id: str):
        """Remove a filter from the current FQL Generator object by filter ID."""
        if filter_id in self.filters:
            del self.filters[filter_id]
        else:
            raise KeyError(f"The filter with ID {filter_id} does not exist in this object.")

    def create_new_filter(
        self,
        filter_name: str,
        initial_value: Any,
        initial_operator: Optional[str] = None,
    ) -> str:
        """Create a new FQL filter and store it, alongside its arguments, inside this object."""
        # For compatability reasons, we must send all filter names to lower case.
        filter_name = filter_name.lower()
        if filter_name not in self.available_filters:
            raise ValueError(f"The specified filter name {filter_name} does not exist.")

        new_filter_def: Dict[str, Any] = self.available_filters[filter_name]

        # Perform simple validations before we execute a validation function
        valid_operators: List[str] = new_filter_def["valid_operators"]
        nullable: bool = new_filter_def["nullable"]

        if initial_operator is None:
            initial_operator = new_filter_def["operator"]
        elif initial_operator not in valid_operators:
            raise ValueError(
                f"The provided initial operator, {initial_operator}, is not valid. Valid "
                f"options for a {filter_name} filter: {str(valid_operators)}"
            )

        # Ensure the initial value provided is of the right data type
        self._validate_input_type(
            filter_name=filter_name,
            filter_def=new_filter_def,
            value=initial_value,
        )

        # If the input is None, and we're nullable, we can just skip the rest
        if nullable and initial_value is None:
            transformed_value = None
        else:
            transformed_value = self._validate_and_transform(
                filter_name=filter_name,
                filter_def=new_filter_def,
                value=initial_value,
            )

        fql = new_filter_def["fql"]

        filter_args = FilterArgs(
            filter_def=filter_name, fql=fql, value=transformed_value, operator=initial_operator
        )
        return self.add_filter(filter_args)

    def create_new_filter_from_kv_string(self, key_string: str, value) -> str:
        """
        Create a filter from a key->value string.

        Examples:
        -> Domain__NOT=ExcludeDomain.com
        -> LastSeen__GTE=1970-01-01T00:00:00Z
        """
        if "__" in key_string:
            filter_name, operator = key_string.split("__")
        else:
            filter_name = key_string
            operator = None  # None operator results in the default

        if isinstance(value, str):
            if "," in value:
                value = value.split(",")

        if operator:
            return self.create_new_filter(
                filter_name=filter_name, initial_value=value, initial_operator=operator
            )

        return self.create_new_filter(filter_name=filter_name, initial_value=value)

    def get_fql(self) -> str:
        """Return a valid FQL string based on the filters within this object."""
        fql_strings: List[str] = []
        for filter_args in self.filters.values():
            operator_symbol = FILTER_OPERATORS[filter_args.operator]

            if (
                isinstance(filter_args.value, list)
                and filter_args.value
                and isinstance(filter_args.value[0], str)
            ):
                fql_value = "['" + "','".join(filter_args.value) + "']"
            elif isinstance(filter_args.value, list):
                fql_value = "[" + ",".join(filter_args.value) + "]"
            elif isinstance(filter_args.value, str):
                if filter_args.value.lower() in ["true", "false"]:
                    fql_value = filter_args.value.lower()
                else:
                    fql_value = f"'{filter_args.value}'"
            elif isinstance(filter_args.value, bool):
                fql_value = str(filter_args.value).lower()
            elif filter_args.value is None:
                fql_value = "null"
            else:
                fql_value = str(filter_args.value)

            fql_string = f"{filter_args.fql}: {operator_symbol}{fql_value}"
            fql_strings.append(fql_string)

        return "+".join(fql_strings)

    def __str__(self) -> str:
        """Return an FQL string representation of the FQLGenerator object's contents."""
        return self.get_fql()
