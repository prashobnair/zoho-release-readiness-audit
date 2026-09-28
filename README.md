# zoho-release-readiness-audit (moved)

This project moved to [zoho-implementation-toolkit](https://github.com/prashobnair/zoho-implementation-toolkit) as the `release` module. Its full commit history was preserved there.

It compares before/after configuration manifests so a release review catches added, removed, and broken pieces before ship.

## Use it now

```sh
pip install https://github.com/prashobnair/zoho-implementation-toolkit/releases/download/v0.1.0/zohokit-0.1.0-py3-none-any.whl
```

or

```sh
uv tool install git+https://github.com/prashobnair/zoho-implementation-toolkit@v0.1.0
```

The old `python cli.py manifest.json [--strict]` is now:

```sh
zohokit release diff before-after.json [--strict]
```

`--strict` exits 2 when the release is not ready. Reports render with `--format json|table|markdown|html` and `--out`.

## Links

- Module guide: https://prashobnair.github.io/zoho-implementation-toolkit/modules/release/
- What changed versus this repo: https://prashobnair.github.io/zoho-implementation-toolkit/legacy-parity/
- Source: https://github.com/prashobnair/zoho-implementation-toolkit/tree/main/src/zohokit/modules/release

This repository is archived and read-only.
