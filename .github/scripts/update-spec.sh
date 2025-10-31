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

# Add changelog entry manually (rpmdev-bumpspec not available on Ubuntu)
echo "Adding changelog entry..."
CHANGELOG_DATE=$(date "+%a %b %d %Y")

# Find the %changelog section and insert the new entry
# Use a temp file to avoid sed multi-line issues
TEMP_FILE="${SPEC_FILE}.tmp"
awk -v date="$CHANGELOG_DATE" -v version="$NEW_VERSION" '
/^%changelog/ {
    print $0
    print "* " date " Automated Update <noreply@github.com> - " version "-1"
    print "- Update to " version
    print ""
    next
}
{ print }
' "$SPEC_FILE" > "$TEMP_FILE"
mv "$TEMP_FILE" "$SPEC_FILE"

# Also reset Release number to 1
sed -i "s/^Release:\s*.*/Release:        1%{?dist}/" "$SPEC_FILE"

echo "Spec file updated successfully"

# Show the changes
echo ""
echo "=== Changes made ==="
git diff "$SPEC_FILE" || true
