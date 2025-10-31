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
# Handle both direct URLs and macros
SOURCE_LINE=$(grep "^Source0:" "$SPEC_FILE" | head -1)
SOURCE_VALUE=$(echo "$SOURCE_LINE" | awk '{print $2}')

# Check if using %{forgesource} macro
if echo "$SOURCE_VALUE" | grep -q "%{forgesource}"; then
    # Extract forgeurl and version to construct the archive URL
    FORGEURL=$(grep "^%global forgeurl" "$SPEC_FILE" | awk '{print $3}')
    VERSION=$(grep "^Version:" "$SPEC_FILE" | head -1 | awk '{print $2}')

    # Handle empty VERSION (might be using %forgemeta or other macros)
    if [ -z "$VERSION" ] || [ "$VERSION" = "%{version}" ]; then
        VERSION=$(grep -E "^Version:|%global.*version" "$SPEC_FILE" | grep -v forgemeta | head -1 | awk '{print $NF}')
    fi

    if [ -z "$FORGEURL" ]; then
        echo "Error: Using forgesource but no forgeurl found"
        exit 1
    fi

    # Construct GitHub archive URL from forgeurl
    # Try with 'v' prefix first (most common), then without, then refs/tags/
    SOURCE_URL="${FORGEURL}/archive/v${VERSION}.tar.gz"

    # Quick check if URL is accessible, try alternative formats if not
    HTTP_CHECK=$(curl -s -o /dev/null -w "%{http_code}" -L -I "$SOURCE_URL" 2>/dev/null || echo "000")
    if [ "$HTTP_CHECK" != "200" ] && [ "$HTTP_CHECK" != "302" ]; then
        # Try without 'v' prefix
        SOURCE_URL="${FORGEURL}/archive/${VERSION}.tar.gz"
        HTTP_CHECK=$(curl -s -o /dev/null -w "%{http_code}" -L -I "$SOURCE_URL" 2>/dev/null || echo "000")

        if [ "$HTTP_CHECK" != "200" ] && [ "$HTTP_CHECK" != "302" ]; then
            # Try refs/tags/ format
            SOURCE_URL="${FORGEURL}/archive/refs/tags/${VERSION}.tar.gz"
        fi
    fi
else
    # Extract the URL, handling %{url}, %{forgeurl}, %{version}, etc.
    URL_BASE=$(grep "^URL:" "$SPEC_FILE" | awk '{print $2}')
    FORGEURL=$(grep "^%global forgeurl" "$SPEC_FILE" | awk '{print $3}')
    VERSION=$(grep "^Version:" "$SPEC_FILE" | head -1 | awk '{print $2}')

    # Handle empty VERSION
    if [ -z "$VERSION" ] || [ "$VERSION" = "%{version}" ]; then
        VERSION=$(grep -E "^Version:|%global.*version" "$SPEC_FILE" | grep -v forgemeta | head -1 | awk '{print $NF}')
    fi

    # Use forgeurl if available, otherwise use URL
    if [ -n "$FORGEURL" ]; then
        URL_BASE="$FORGEURL"
    fi

    # Simple macro substitution for common patterns
    SOURCE_URL=$(echo "$SOURCE_VALUE" | \
        sed "s|%{url}|${URL_BASE}|g" | \
        sed "s|%{forgeurl}|${URL_BASE}|g" | \
        sed "s|%{version}|${VERSION}|g" | \
        sed "s|%{name}|${PACKAGE_NAME}|g")
fi

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
