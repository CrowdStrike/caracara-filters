"""Caracara Filters: FQL Class.

This file contains a class that can be instantiated to contain filters. It must be configured with
a dialect, after which filters can be added.
"""
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Type, Optional
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

    filter_type: str
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

    def __init__(self, dialect: str = 'base'):
        """Create a new FQL generator with a specific dialect."""
        if dialect not in DIALECTS:
            raise ValueError(
                f"The specified dialect does not exist. Valid choices are: {str(DIALECTS.keys())}."
            )

        if dialect == 'base':
            self.available_filters: Dict[str, Dict[str, Any]] = DIALECTS['base']
        else:
            self.available_filters: Dict[str, Dict[str, Any]] = {
                **DIALECTS['base'],
                **DIALECTS[dialect],
            }

        self.dialect: str = dialect
        self.filters: Dict[str, FilterArgs] = {}

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

        new_filter_type: Dict[str, Any] = self.available_filters[filter_name]

        # Perform simple validations before we execute a validation function
        valid_operators: List[str] = new_filter_type['valid_operators']
        multivariate: bool = new_filter_type['multivariate']
        data_type: Type = new_filter_type['data_type']

        if initial_operator is None:
            initial_operator = new_filter_type['operator']
        elif initial_operator not in valid_operators:
            raise ValueError(
                f"The provided initial operator, {initial_operator}, is not valid. Valid "
                f"options for a {filter_name} filter: {str(valid_operators)}"
            )

        if isinstance(initial_value, list):
            if (
                multivariate is True and
                initial_value and
                not isinstance(initial_value[0], data_type)
            ):
                raise TypeError(
                    f"You provided a list for {filter_name}, but the type of the first item was "
                    f"{str(type(initial_value))}, which is not a {str(type(data_type))}."
                )
            if multivariate is False:
                raise TypeError(
                    f"The filter {filter_name} is not multivariate, but you provided a list."
                )
        else:
            if not isinstance(initial_value, data_type):
                raise TypeError(
                    f"The filter {filter_name} expects a {str(type(data_type))} type, but you "
                    f"provided an initial value of type {str(type(initial_value))}."
                )

        # Run through the validation function
        validation_func: Callable[[Any], bool] = new_filter_type['validator']
        if not validation_func(initial_value):
            raise ValueError(
                f"The input {initial_value} is not valid for filter type {filter_name}."
            )

        # Transform the input
        transform_func: Callable[[Any], Any] = new_filter_type['transform']
        transformed_value = transform_func(initial_value)

        fql = new_filter_type['fql']

        filter_args = FilterArgs(
            filter_type=filter_name,
            fql=fql,
            value=transformed_value,
            operator=initial_operator
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
            if ',' in value:
                value = value.split(',')

        if operator:
            return self.create_new_filter(
                filter_name=filter_name,
                initial_value=value,
                initial_operator=operator
            )

        return self.create_new_filter(
            filter_name=filter_name,
            initial_value=value
        )

    def get_fql(self) -> str:
        """Return a valid FQL string based on the filters within this object."""
        fql_strings: List[str] = []
        for filter_args in self.filters.values():
            operator_symbol = FILTER_OPERATORS[filter_args.operator]

            # Handle empty values with a null, then loop back round and ignore the rest of the logic
            if filter_args.value is None:
                fql_strings.append(f'{filter_args.fql}:{operator_symbol}null')
                continue

            if (
                isinstance(filter_args.value, list) and
                filter_args.value and
                isinstance(filter_args.value[0], str)
            ):
                fql_value = "['" + "','".join(filter_args.value) + "']"
            elif isinstance(filter_args.value, list):
                fql_value = '[' + ','.join(filter_args.value) + ']'
            elif isinstance(filter_args.value, str):
                if filter_args.value.lower() in ['true', 'false']:
                    fql_value = filter_args.value.lower()
                else:
                    fql_value = f"'{filter_args.value}'"
            elif isinstance(filter_args.value, bool):
                fql_value = str(filter_args.value).lower()
            else:
                fql_value = str(filter_args.value)

            fql_string = f'{filter_args.fql}: {operator_symbol}{fql_value}'
            fql_strings.append(fql_string)

        return '+'.join(fql_strings)

    def __str__(self) -> str:
        """Return an FQL string representation of the FQLGenerator object's contents."""
        return self.get_fql()
