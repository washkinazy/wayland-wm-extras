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

# Basic syntax validation - check for required fields
echo "Checking spec file for required fields..."
for field in Name Version Release Summary License URL Source0; do
    if ! grep -q "^${field}:" "$SPEC_FILE"; then
        echo "Error: Missing required field: $field"
        exit 1
    fi
done

# Extract key information using grep/sed (more portable than rpmspec)
NAME=$(grep "^Name:" "$SPEC_FILE" | head -1 | awk '{print $2}')
VERSION=$(grep "^Version:" "$SPEC_FILE" | head -1 | awk '{print $2}')

# Handle empty VERSION (might be using %forgemeta or other macros)
if [ -z "$VERSION" ] || [ "$VERSION" = "%{version}" ]; then
    # Try to find version in other ways
    VERSION=$(grep -E "^Version:|%global.*version" "$SPEC_FILE" | grep -v forgemeta | head -1 | awk '{print $NF}')
fi

RELEASE=$(grep "^Release:" "$SPEC_FILE" | head -1 | awk '{print $2}')

echo ""
echo "=== Validation successful ==="
echo "Package: $NAME"
echo "Version: $VERSION"
echo "Release: $RELEASE"
echo "Full NVR: $NAME-$VERSION-$RELEASE"
