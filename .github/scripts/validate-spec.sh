#!/bin/bash
set -e

# Script to validate RPM spec file
# Usage: validate-spec.sh <spec_dir> <package_name>

SPEC_DIR="$1"
PACKAGE_NAME="$2"

if [ -z "$SPEC_DIR" ] || [ -z "$PACKAGE_NAME" ]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 <spec_dir> <package_name>"
    exit 1
fi

SPEC_FILE="${SPEC_DIR}/${PACKAGE_NAME}.spec"

if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: Spec file not found: $SPEC_FILE"
    exit 1
fi

echo "Validating spec file: $SPEC_FILE"

# Check spec file syntax with rpmspec -q
echo "Checking spec file syntax..."
if ! rpmspec -q --qf "%{name}-%{version}-%{release}\n" "$SPEC_FILE" > /dev/null 2>&1; then
    echo "Error: Spec file has syntax errors"
    rpmspec -q --qf "%{name}-%{version}-%{release}\n" "$SPEC_FILE"
    exit 1
fi

# Verify spec can be parsed with rpmspec -P
echo "Verifying spec file can be parsed..."
if ! rpmspec -P "$SPEC_FILE" > /dev/null 2>&1; then
    echo "Error: Spec file cannot be parsed"
    rpmspec -P "$SPEC_FILE"
    exit 1
fi

# Extract and display key information
NAME=$(rpmspec -q --qf "%{name}\n" "$SPEC_FILE" 2>/dev/null | head -1)
VERSION=$(rpmspec -q --qf "%{version}\n" "$SPEC_FILE" 2>/dev/null | head -1)
RELEASE=$(rpmspec -q --qf "%{release}\n" "$SPEC_FILE" 2>/dev/null | head -1)

echo ""
echo "=== Validation successful ==="
echo "Package: $NAME"
echo "Version: $VERSION"
echo "Release: $RELEASE"
echo "Full NVR: $NAME-$VERSION-$RELEASE"
