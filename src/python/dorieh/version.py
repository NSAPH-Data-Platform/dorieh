#  Copyright (c) 2024. Harvard University
#
#  Developed by Research Software Engineering,
#  Harvard University Research Computing and Data (RCD) Services.
#
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#
#
#
#
#
#  Developed by Research Software Engineering,
#  Harvard University Research Computing and Data (RCD) Services.
#
#  Author: Michael A Bouzinier
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#           http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
import json
import sys
from importlib.metadata import version, distribution


PACKAGE_NAME = "dorieh"
VERSION = None


def get_version() -> str:
    global VERSION
    if VERSION:
        return VERSION
    package_version = None
    url = None
    sha = None
    try:
        package_version = version(PACKAGE_NAME)
    except:
        pass
    try:
        d1 = distribution(PACKAGE_NAME)
        url_json = d1.read_text("direct_url.json")
        if url_json:
            data = json.loads(url_json)
            if "url" in data:
                url = data["url"]
            if sha is None and "vcs_info" in data:
                vcs_info = data["vcs_info"]
                if "commit_id" in vcs_info:
                    sha = vcs_info["commit_id"]
        if not url:
            url = d1.metadata.get("Home-page")
    except:
        pass
    if not sha:
        stdout = sys.stdout
        sys.stdout = open('/dev/null', 'w')
        try:
            import git
            #sys.stdout = stdout
            repo = git.Repo(path=__file__, search_parent_directories=True)
            sha = repo.head.object.hexsha
        except Exception as x:
            pass
        sys.stdout = stdout
    info = {
        "version": package_version,
        "url": url,
        "commit": sha
    }
    VERSION = json.dumps(info)
    return VERSION


def main():
    print(get_version())


if __name__ == '__main__':
    main()
