#!/usr/bin/env bash
# Compatibility entry point; the Python implementation validates every value.
set -euo pipefail
exec python3 - "$(dirname "$0")" "$@" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, sys.argv[1])
from packages import update_spec
args = sys.argv[2:]
if len(args) < 4:
    raise SystemExit('Usage: update-spec.sh SPEC_DIR PACKAGE VERSION TAG [MODE [SHORT_SHA]]')
directory, package, version, tag, *rest = args
update_spec(Path(directory) / (package + '.spec'), version, tag, rest[0] if rest else 'release')
PY
