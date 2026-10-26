#!/usr/bin/env bash
set -euo pipefail
branch="auto-update/$PACKAGE"
title="chore: update $PACKAGE to $VERSION"
git config --global --add safe.directory "$PWD"
git config user.name 'github-actions[bot]'
git config user.email '41898282+github-actions[bot]@users.noreply.github.com'
# Resolve the existing remote branch before using a lease; never overwrite a race.
git -c credential.helper= -c 'credential.helper=!gh auth git-credential' fetch origin "+refs/heads/$branch:refs/remotes/origin/$branch" 2>/dev/null || {
    # Only a missing branch is acceptable, not an authentication or network failure.
    refs=$(git -c credential.helper= -c 'credential.helper=!gh auth git-credential' ls-remote --heads origin "$branch")
    test -z "$refs"
}
git checkout -B "$branch"
git add -- "$PACKAGE/$PACKAGE.spec"
git commit -m "$title"
git -c credential.helper= -c 'credential.helper=!gh auth git-credential' push --force-with-lease origin "HEAD:refs/heads/$branch"
body=$(mktemp)
trap 'rm -f "$body"' EXIT
cat > "$body" <<EOF
Updates $PACKAGE from $PREVIOUS to $VERSION.

The Fedora RPM parser and exact source downloads passed. Package builds run in
PR CI. Review the build results before merging; this workflow never bypasses
branch protection or merges the PR itself.
EOF
number=$(gh pr list --head "$branch" --base main --state open --json number --jq '.[0].number // empty')
if [ -n "$number" ]; then
    gh pr edit "$number" --title "$title" --body-file "$body"
else
    gh pr create --base main --head "$branch" --title "$title" --body-file "$body"
fi
