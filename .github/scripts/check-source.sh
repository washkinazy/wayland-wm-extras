#!/usr/bin/env bash
set -euo pipefail
exec python3 "$(dirname "$0")/sources.py" "${1:?Missing spec directory}/${2:?Missing package}.spec"
