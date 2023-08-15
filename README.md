![CrowdStrike Falcon](https://raw.githubusercontent.com/CrowdStrike/falconpy/main/docs/asset/cs-logo.png) [![Twitter URL](https://img.shields.io/twitter/url?label=Follow%20%40CrowdStrike&style=social&url=https%3A%2F%2Ftwitter.com%2FCrowdStrike)](https://twitter.com/CrowdStrike)<br/>

# Caracara Filters

[![PyPI](https://img.shields.io/pypi/v/caracara-filters)](https://pypi.org/project/caracara-filters/)
![OSS Lifecycle](https://img.shields.io/osslifecycle/CrowdStrike/caracara-filters)

A new filter system for Caracara.

Caracara's previous filter system was inflexible, and tailored too heavily toward the Hosts API module. This project aims to provide an FQL generator that is dialect-aware (i.e., contextual, based on the API module that the request will be sent to).

## Basic Concepts

Instead of declaring each filter as a class, we now have them defined in a dictionary which is significantly easier to work with. Dynamic functionality is provided by storing (partial) functions into each filter.

Each filter derives from the 'default' / base filter, which is configured with identity transforms and validators that return the input value and `True`, respectively, and expects a string input. These settings can be overridden per-filter, and are enforced when a filter is added to the `FQLGenerator` object. We call this process rebasing, as each filter is rebased from a smaller dictionary over the top of the default filter, thus ensuring that all expected values will be present.

When a filter is created, the input goes through these processing stages:

- Validation: the filter's input is passed into a validation function that always returns a `bool`. `True` means that the input is valid, and `False` will raise a `ValueError` exception. At this stage, we also validate the input type; incorrect input types will result in a `TypeError`.
- Transformation: each filter value can be transformed from a human-defined input into something machine-readable, expected by the API. For example, relative timestamps (such as `-30m`) are transformed to a UTC ISO8601 timestamp ready for the Falcon API, and `Containment Pending` is rewritten to `containment_pending` as expected by the Hosts API.
- Storage: the validated, transformed input is stored alongside the FQL property name and the operator (e.g., equality, `>=`, etc.), ready for FQL generation.

When FQL is generated, each of the filters are iterated over and converted to FQL individually, and then chained together with `+` to form an `AND` condition.

## Limitations

We currently only support a limited subset of FQL. For example:

- We *can* generate a condition like "all systems that run Windows or Linux, AND have an IP address in the range 192.168.0.0/16 OR 10.0.0.0/8".
- We *cannot* generate a condition like "all systems that run Windows AND have an IP address in the 192.168.0.0/16 range, as well as all Linux systems in the 10.0.0.0/8 range".

The latter is out of scope as it requires chaining together multiple filters. You can effectively create this functionality for yourself by creating two FQL generators, wrapping their outputs in parentheses, and chaining them together with a `'+'.join()`.

