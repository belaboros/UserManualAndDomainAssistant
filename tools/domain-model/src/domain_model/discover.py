"""Find the domain folders of the repo: folders holding both ontology.yaml and statements.yaml.

Hidden folders, ``tests/`` folders (fixtures) and ``generated/`` folders are skipped.
"""

from __future__ import annotations

import os
from pathlib import Path

from domain_model.load import ONTOLOGY, STATEMENTS

SKIPPED = {"tests", "generated", "node_modules", "__pycache__"}


def discover(root: Path) -> list[Path]:
    """Every domain folder under ``root``, sorted."""
    found = []
    for directory, subdirs, files in os.walk(root):
        subdirs[:] = sorted(d for d in subdirs if not d.startswith(".") and d not in SKIPPED)
        if ONTOLOGY in files and STATEMENTS in files:
            found.append(Path(directory))
    return sorted(found)
