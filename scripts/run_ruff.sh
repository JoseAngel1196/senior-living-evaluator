#!/bin/bash

set -eo pipefail

poetry run ruff format .
poetry run ruff check --fix --exit-non-zero-on-fix .
