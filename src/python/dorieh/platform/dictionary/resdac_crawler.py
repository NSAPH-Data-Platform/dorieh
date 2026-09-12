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
import datetime
import os.path
import re
import sys
import time
from typing import Dict

import requests
import yaml
from googlesearch import search


GOOGLE_API_KEY = ""
CSE_ID = ''


MANUAL_MAP = {
    "BENE_HMO_IND": "https://resdac.org/cms-data/variables/hmo-indicator",
    "BENE_MDCR_ENTLMT_BUYIN_IND": "https://resdac.org/cms-data/variables/medicare-entitlementbuy-indicator",
    "BUYIN": "https://resdac.org/cms-data/variables/medicare-entitlementbuy-indicator",
    "BENE_AGE_AT_END_REF_YR": "https://resdac.org/cms-data/variables/age-beneficiary-end-year",
    "BENE_MDCR_STATUS_CD": "https://resdac.org/cms-data/variables/reason-entitlement-medicare-benefits-clmthrudt"
}


last_request = datetime.datetime.now()

def google_search(search_term, api_key, cse_id, **kwargs):
    url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        'q': search_term,
        'key': api_key,
        'cx': cse_id,
    }
    params.update(kwargs)
    now = datetime.datetime.now()
    global last_request
    if (now - last_request).total_seconds() < 1:
        time.sleep(1)
    response = requests.get(url, params=params)
    last_request = datetime.datetime.now()
    response.raise_for_status()
    return response.json()


URL_CACHE = dict()
URL_CACHE.update(MANUAL_MAP)


def get_resdac_url(column_name):
    if column_name in URL_CACHE:
        return URL_CACHE[column_name]
    
    query = f'ResDac "{column_name}"'
    print(f'Searching for: {query}')
    try:
        results = google_search(query, GOOGLE_API_KEY, CSE_ID)
        for item in results.get('items', []):
            link = item["link"]
            if 'resdac.org/cms-data/variables/' in link:
                URL_CACHE[column_name] = link
                return link
        URL_CACHE[column_name] = None
        return None
    except Exception as e:
        print(f"Error searching for {query}: {e}")
        return None


def get_resdac_url_free(column_name):
    """
    Function to search for the ResDac description URL given a column name

    :param column_name:
    :return:
    """

    query = f'ResDac "{column_name}"'
    print(f'Searching for: {query}')
    try:
        # Search on Google
        search_results = search(query, num_results=10)
        for result in search_results:
            if 'resdac.org/cms-data/variables/' in result:
                return result
        return None
    except Exception as e:
        print(f"Error searching for {query}: {e}")
        return None


class ColumnInfo:
    def __init__(self, name):
        self.name = name
        self.description = None
        self.url = None


def extract_prefix_for_month(input_string):
    pattern = r"(.+)_([0][1-9]|1[0-2])$"
    match = re.match(pattern, input_string)
    if match:
        return match.group(1)
    return None


NOT_FOUND = set()


def get_resdac_mapping(search = False, update = False) -> Dict[str, ColumnInfo]:
    """
    Parse Model YaML file and create a mapping between column names and column metadata.
    Optionally, search Google for a URL to ResDac description for a column.


    :return:
    """

    column_map: Dict[str, ColumnInfo] = dict()
    p = os.path.join(os.path.dirname(__file__), "../../cms/models/medicare_cms.yaml")
    with open(p) as f:
        model = yaml.safe_load(f)

    tables = model["cms"]["tables"]
    for t in tables:
        for col in tables[t].get("columns", []):
            if isinstance(col, str):
                c = col
                val = None
            elif isinstance(col, dict):
                c = list(col.keys())[0]
                val = col[c]
            else:
                continue
            c = c.lower()
            if c in column_map:
                continue
            column = ColumnInfo(c)
            name = c
            if val and "description" in val:
                column.description = val["description"]
                if "long_name" in column.description:
                    name = column.description["long_name"]

            if val and "reference" in val:
                column.url = val["reference"]
            if search and column.url is None:
                url = get_resdac_url(name)
                if not url:
                    prefix = extract_prefix_for_month(name)
                    if prefix:
                        url = get_resdac_url(prefix)
                if url:
                    column.url = url
                    val["reference"] = url
                    print(url)
                else:
                    print(f"No URL found for {name}")
                    NOT_FOUND.add(name)

            column_map[c] = column

    # Print or save the mapping dictionary
    for column_name, info in column_map.items():
        print(f"{column_name}: {info.url}")

    if update:
        print("Updating YaML")
        for t in tables:
            for col in tables[t].get("columns", []):
                if isinstance(col, dict):
                    c = list(col.keys())[0]
                    val = col[c]
                    c = c.lower()
                    # if c in ["file", "record"]:
                    #     del val["reference"]
                    # elif c in column_map:
                    if c in column_map:
                        val["reference"] = column_map[c].url
        with open(p, "wt") as f:
            yaml.safe_dump(model, f)

    print("Not found:")
    for name in sorted(NOT_FOUND):
        print(name)

    return column_map


if __name__ == '__main__':
    GOOGLE_API_KEY = sys.argv[1]
    CSE_ID = sys.argv[2]
    get_resdac_mapping(True, True)
