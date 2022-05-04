# automation-common

This library contains common utilities for ValidatedAutomation across Avrae services.

## Installation

```bash
pip install git+https://github.com/avrae/automation-common.git@vX.Y.Z
```

## Submodules

### validation

Use `validation.validate(some_dict)` to ensure that the dict can be parsed as valid Automation.

## Versioning

The major and minor versions of `automation-common` should match the major and minor versions of `avrae` for each
Avrae update that changes the automation engine. If a minor Avrae release contains no automation engine updates,
the `automation-common` version may stay the same.

The patch version of `automation-common` may update as needed to reflect patch-level fixes specific
to `automation-common`.

The `automation-common` version is allowed to skip versions to maintain these constraints, but a newer release must not
have a lower version than a prior release.

To release a new version of `automation-common`, update `setup.py` and tag the commit to release with `vX.Y.Z`.
