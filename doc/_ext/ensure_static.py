#  Copyright (c) 2026. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Guarantee that the HTML output's ``_static`` directory exists before
``build-finished`` handlers run.

Under Sphinx 8.2 the copying of static files became a deferred "finish
task", so extensions whose ``build-finished`` handlers write into
``<outdir>/_static`` (notably ``sphinx_paramlinks.copy_stylesheet``) can
fire before the directory exists and crash the build with
``FileNotFoundError: .../docs/_static/sphinx_paramlinks.css``.
Sphinx 9 restored the ordering, but this shim makes the build immune to
the Sphinx version in use.

The handler is registered with priority 400 (default is 500, lower runs
first), so it always precedes the other ``build-finished`` handlers.
"""
import os


def _ensure_static_dir(app, exception):
    builder = getattr(app, "builder", None)
    if builder is not None and getattr(builder, "format", None) == "html":
        os.makedirs(os.path.join(builder.outdir, "_static"), exist_ok=True)


def setup(app):
    app.connect("build-finished", _ensure_static_dir, priority=400)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
