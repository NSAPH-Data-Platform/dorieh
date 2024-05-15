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
from importlib.metadata import version, distribution


PACKAGE_NAME = "dorieh"


def get_version() -> str:
    package_version = None
    url = None
    sha = None
    try:
        package_version = version(PACKAGE_NAME)
    except:
        pass
    try:
        d1 = distribution("dorieh")
        url_json = d1.read_text("direct_url.json")
        if url_json:
            data = json.loads(url_json)
            if "url" in data:
                url = data["url"]
            if "vcs_info" in data:
                vcs_info = data["vcs_info"]
                if "commit_id" in vcs_info:
                    sha = vcs_info["commit_id"]
    except:
        pass
    if not sha:
        try:
            import git
            repo = git.Repo(search_parent_directories=True)
            sha = repo.head.object.hexsha
        except:
            pass
    info = {
        "version": package_version,
        "url": url,
        "sha": sha
    }
    return json.dumps(info)


def main():
    print(get_version())


if __name__ == '__main__':
    main()
