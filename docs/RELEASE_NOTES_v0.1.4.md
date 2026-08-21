# ACE v0.1.4 - license file

## Purpose

This release does not change assessment behaviour, the evidence schema, or any Token-Bleed
verdict. It exists so that the installed package carries the license it has always declared.

## Changes

- Adds the MIT `LICENSE` file to the repository and to the built distributions.

`pyproject.toml` has declared `license = "MIT"` since before 0.1.3, and PyPI recorded
`License-Expression: MIT`, but no license text shipped in the wheel or sdist and the repository
reported as unlicensed. Anyone asked to install this package in order to independently verify a
published evidence packet had no license to do so. The wheel built from this release carries
`dist-info/licenses/LICENSE` alongside `License-Expression: MIT` and `License-File: LICENSE`.

## Compatibility and claim boundary

The retained-evidence JSON schema remains `1.0`. Generic and claim-scoped verdicts for the public
R3 and R5 packets are unchanged by this release.

One field does change: evidence records and CLI output stamp `package_version`, so artifacts
generated with this release record `0.1.4` rather than `0.1.3`. Previously generated artifacts are
not affected, and the recorded value does not participate in any acceptance rule.

Reproductions pinned to an earlier version stay valid. Token-Bleed R5 was assessed with
`ace-experiment-framework==0.1.2` and that pin is deliberate; do not repoint it at this release.
