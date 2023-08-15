# caracara-filters

A new filter dialect for Caracara

Caracara's previous filter system was inflexible, and tailored too heavily toward the Hosts API module. This project aims to build FQL that is dialect-aware (i.e., contextual, based on the API module that the request will be sent to).

Each filter goes through multiple stages:

- Rebasing: at creation, the filter is played over the top of the default filter.
- Validation: the filter's input is tested for the right date type and, where relevant, a sensible input.
- Transform: a valid input is transformed into a valid FQL representation.
- FQL generation: the FQL string is generated.
