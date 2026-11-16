from pathlib import Path
import os
import sys

_REPO_ROOT = Path(__file__).resolve().parents[1]
_WORKSPACE_ROOT = _REPO_ROOT.parent
sys.path.insert(0, str(_REPO_ROOT / "src"))

from photon_platform.publish.global_conf import *
import geometor.russell as module

version = module.__version__

org = "geometor"
org_name = "GEOMETOR"

repo = "russell"
repo_name = "russell"

setup_globals(org, org_name, repo, repo_name)

# Restrict intersphinx_mapping strictly to offline local inventories present on disk:
for _key in list(intersphinx_mapping.keys()):
    _entry = intersphinx_mapping[_key]
    _target = _entry[1] if isinstance(_entry, tuple) and len(_entry) >= 2 else None
    _local_file = _target[0] if isinstance(_target, tuple) and _target else _target
    if not (isinstance(_local_file, str) and Path(_local_file).is_file()):
        intersphinx_mapping.pop(_key, None)

site_title = "Walter & Lao Russell"
project = site_title
html_title = f"{site_title} • {org_name}"
author = "Walter and Lao Russell"
copyright = "1950–1952, Walter and Lao Russell • Digital Edition GEOMETOR"

autoapi_add_toctree_entry = False
suppress_warnings = ["autoapi.python_import_resolution", "toc.not_included"]

def setup(app):
    app.add_js_file("js/russell_3d_codex.js")
