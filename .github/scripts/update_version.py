"""Update the manifest file."""

import json
import sys


def update_manifest() -> None:
    """Update the manifest file."""
    version = "0.0.0"
    manifest_file = ""
    for index, value in enumerate(sys.argv):
        if value in ["--version", "-V"]:
            version = sys.argv[index + 1]
        if value in ["--manifest-file", "-M"]:
            manifest_file = sys.argv[index + 1]

    with open(manifest_file, encoding="utf-8") as manifestfile:
        base: dict = json.load(manifestfile)
        base["version"] = version

    with open(manifest_file, "w", encoding="utf-8") as manifestfile:
        manifestfile.write(
            json.dumps(
                {
                    "domain": base["domain"],
                    "name": base["name"],
                    **{k: v for k, v in sorted(base.items()) if k not in ("domain", "name")},
                },
                indent=4,
            )
        )


update_manifest()
