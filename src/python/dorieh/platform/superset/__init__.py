#  Copyright (c) 2026. Harvard University
#
#  Developed by Research Software Engineering,
#  Faculty of Arts and Sciences, Research Computing (FAS RC)
#  Author: Michael A Bouzinier
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

"""Superset integration utilities for Dorieh.

Export and import Apache Superset dashboards as native (ZIP/YAML) bundles,
re-pointing a bundle onto a local database connection that is resolved BY NAME
at import time (each Superset instance assigns its own connection uuid, so a
committed bundle cannot hard-code it). Exposed as the ``superset_export`` and
``superset_import`` console scripts.
"""

from dorieh.platform.superset.api import SupersetClient  # noqa: F401
