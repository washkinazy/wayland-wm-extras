# wayland-wm-extras

RPM packaging for fonts, tools, and utilities used on Fedora Wayland systems.
Packages are published through the `washkinazy/wayland-wm-extras` COPR.

## Packages and installation

[packages.yml](packages.yml) is the authoritative package inventory. Each entry
has a matching directory and spec file. Run `just list` for package names.
Entries with `update: false` are maintained manually: `gtklock-meta` has no
upstream payload, and `xone-firmware` changes only when its firmware payloads
change, independently of the driver repository.

```bash
sudo dnf copr enable washkinazy/wayland-wm-extras
sudo dnf install walker elephant gtklock
```

## Updates and validation

The daily workflow checks upstream releases at midnight UTC. The **Update Single
Package** workflow accepts any automatically tracked package name in the
inventory; invalid names fail before any update or write credentials are used.
Both manual workflows support `force_update`, which increments `Release` when
the upstream revision is unchanged. Older releases are never treated as updates.
Unsupported tag formats fail explicitly for maintainer review.

Release packages use RPM version ordering. Branch-tracked packages compare the
full commit SHA and use ordered timestamp snapshots under the current version
base. When moving to a new upstream release base, update that base explicitly.
The fallback for repositories without releases selects the greatest stable
numeric version among the first 100 tags returned by GitHub.

Updates are parsed using Fedora's RPM macros. Every declared remote source and
patch is downloaded from its exact expanded HTTPS URL; local sources and patches
must exist inside the package directory. The updater maintains one PR branch per
package and serializes overlapping updates to that package. It never merges PRs.

Pull requests run:

- Inventory consistency checks, regression tests, ShellCheck, and RPM parsing.
- Mock builds of changed packages on Fedora 43 and 44. Changes to shared build
  tooling, tests, or workflows rebuild all packages.
- An aggregate **Package checks** status, suitable for a required check.

Builds use the existing COPR as an additional dependency repository. If an update
needs a dependency version not published there yet, its build will fail until the
dependency is available. Network access is currently required for Rust/Go builds;
Cargo builds require the upstream lockfile, and direct Go builds use read-only
module resolution. This is not an offline or fully hermetic build system.

Merged changes trigger COPR builds if the repository's COPR webhook is configured.

## Development

Use the Fedora 44 dev container, or create a Distrobox environment:

```bash
just setup-44
just enter 44
# Re-enter after setup to activate mock group membership.
just check
just mock xcur2png
```

The setup installs the Fedora RPM macros, Python RPM bindings, PyYAML, ShellCheck,
and packaging tools. It does not change the host's global Mock networking policy.
Build networking is enabled for the individual Mock invocation.

```bash
just mock elephant 43  # Isolated Mock build for one Fedora version
just build walker     # Local rpmbuild; install BuildRequires yourself first
just review gtklock
just build-all 44
just mock-all walker  # Fedora 43 and 44
just build-matrix     # Every package on both versions
just clean            # Remove only this repo's .build directory
```

Each build creates a unique `.build/PACKAGE-fVERSION.XXXXXX` directory containing
sources, the newly generated SRPM, results, and logs. Old SRPMs are never reused.
Batch builds continue after failures and return a nonzero status if any build
fails. The CI container uses Mock's simple chroot isolation inside a disposable
privileged container; normal local builds use nspawn.

To run the updater locally, supply `GH_TOKEN` through your environment, then run
`just update PACKAGE`. Review its diff and build the package before committing.
For a forced rebuild use
`python3 .github/scripts/packages.py update PACKAGE --force`.
