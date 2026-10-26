#!/usr/bin/env bash
set -euo pipefail
spec="${1:?Usage: validate-spec.sh SPEC_DIR PACKAGE}/${2:?Missing package}.spec"
# Fedora's parser expands the same macros used by the build, including forge metadata.
rpmspec -P "$spec" >/dev/null
rpmspec -q --srpm --qf '%{NAME}-%{VERSION}-%{RELEASE}\n' "$spec"
