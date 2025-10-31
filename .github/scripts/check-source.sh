#!/bin/bash
set -e

# Script to check if source tarball is accessible
# Usage: check-source.sh <spec_dir> <package_name>

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

echo "Checking source accessibility for: $SPEC_FILE"

# Extract Source0 URL from spec file
# Handle both direct URLs and macros like %{url}/archive/...
SOURCE_URL=$(rpmspec -P "$SPEC_FILE" 2>/dev/null | grep -E "^Source0?:" | head -1 | awk '{print $2}')

if [ -z "$SOURCE_URL" ]; then
    echo "Error: Could not extract Source0 URL from spec file"
    exit 1
fi

echo "Source URL: $SOURCE_URL"

# Perform HEAD request to check if source is accessible
echo "Checking URL accessibility..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -L -I "$SOURCE_URL" || echo "000")

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "302" ]; then
    echo ""
    echo "=== Source check successful ==="
    echo "HTTP Status: $HTTP_CODE"
    echo "Source tarball is accessible"
else
    echo ""
    echo "=== Source check failed ==="
    echo "HTTP Status: $HTTP_CODE"
    echo "Source tarball is NOT accessible at: $SOURCE_URL"
    exit 1
fi
