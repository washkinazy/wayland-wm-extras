#!/bin/bash
set -e

# Script to update RPM spec file with new version
# Usage: update-spec.sh <spec_dir> <package_name> <new_version> <new_tag>

SPEC_DIR="$1"
PACKAGE_NAME="$2"
NEW_VERSION="$3"
NEW_TAG="$4"

if [ -z "$SPEC_DIR" ] || [ -z "$PACKAGE_NAME" ] || [ -z "$NEW_VERSION" ] || [ -z "$NEW_TAG" ]; then
    echo "Error: Missing required arguments"
    echo "Usage: $0 <spec_dir> <package_name> <new_version> <new_tag>"
    exit 1
fi

SPEC_FILE="${SPEC_DIR}/${PACKAGE_NAME}.spec"

if [ ! -f "$SPEC_FILE" ]; then
    echo "Error: Spec file not found: $SPEC_FILE"
    exit 1
fi

echo "Updating spec file: $SPEC_FILE"
echo "Package: $PACKAGE_NAME"
echo "New version: $NEW_VERSION"
echo "New tag: $NEW_TAG"

# Update Version field
echo "Updating Version field..."
sed -i "s/^Version:\s*.*/Version:        ${NEW_VERSION}/" "$SPEC_FILE"

# Update Source0 URL to use new tag
# Pattern handles: /archive/v1.0.0/ or /archive/refs/tags/v1.0.0/
echo "Updating Source0 URL..."
sed -i "s|/archive/[^/]*/|/archive/${NEW_TAG}/|g" "$SPEC_FILE"
sed -i "s|/archive/refs/tags/[^/]*/|/archive/refs/tags/${NEW_TAG}/|g" "$SPEC_FILE"

# Add changelog entry using rpmdev-bumpspec
echo "Adding changelog entry..."
rpmdev-bumpspec -c "Update to ${NEW_VERSION}" "$SPEC_FILE"

echo "Spec file updated successfully"

# Show the changes
echo ""
echo "=== Changes made ==="
git diff "$SPEC_FILE" || true
