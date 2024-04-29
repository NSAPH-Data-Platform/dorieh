"""
A utility to create skeleton data model (database schema)
for gridMET data
"""

#  Copyright (c) 2021. Harvard University
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
#

import os
import sys
from pathlib import Path
import yaml

from dorieh.platform import init_logging
from dorieh.platform.pg_keywords import PG_NUMERIC_TYPE, PG_DATE_TYPE, PG_STR_TYPE

from dorieh.rasters.config import Geography, GridmetVariable


DATE_COLUMN = "observation_date"
EXTRACT_YEAR = f"(EXTRACT (YEAR FROM {DATE_COLUMN}))::INT"


class Registry:
    """
    This class
    creates YAML data model for gridMET tables.
    """

    COMMON_COLUMNS = f"""
        - year: 
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (EXTRACT (YEAR FROM {DATE_COLUMN})) STORED"
            type: INT
            index: true
            doc: The year of the observation
        - month: 
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (EXTRACT (MONTH FROM {DATE_COLUMN})) STORED"
            type: INT
            index: true
            doc: The year of the observation
        - day_of_the_year: 
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (EXTRACT (DOY FROM {DATE_COLUMN})) STORED"
            type: INT
            index: true
            doc: The year of the observation
    """

    COUNTY_COLUMNS = """
        - fips5:
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (county::INT) STORED"
            type: INT
            doc: County FIPS code as an integer, value is equal to "county".
        - fips2:
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (substring(county, 1, 2)::INT) STORED"
            type: INT
            doc: FIPS code of the US State in which the county is located
        - fips3:
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (substring(county, 3, 3)::INT) STORED"
            type: INT
            doc: FIPS code of the county without state FIPS code
        - state:
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (public.fips2state(substring(county, 1, 2)::VARCHAR)) STORED"
        - state_iso:
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (public.fips2state_iso(substring(county, 1, 2))) STORED"
    """
    ZCTA_COLUMNS = f"""
        - state:
            index: true
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (public.zip_to_state({EXTRACT_YEAR}, zcta::INT)) STORED"
            doc: |
              This column is for informational purposes only. The US State or 
              territory Id associated with this ZCTA. Some ZCTAs span over
              more than one states or territories.
        - city:
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (public.zip_to_city({EXTRACT_YEAR}, zcta::INT)) STORED"
            doc: |
              This column is for informational purposes only. The name 
              of the city preferred by the US Postal service for the ZIP code
              associated with this ZCTA.
        - county:
            source:
              type: "generated"
              code: "GENERATED ALWAYS AS (public.zip_to_fips5({EXTRACT_YEAR}, zcta::INT)) STORED"
            doc: |
              This column is for informational purposes only. The US County  
              FIPS code, for the county having the largest intersection 
              in terms of population with this ZCTA. 
    """

    def __init__(self, destination:str, dn: str = None):
        self.destination = destination
        self.name = dn
        init_logging()

    def update(self):
        with open(self.destination, "wt") as f:
            f.write(self.create_yaml())
        return

    def create_yaml(self):
        domain = {
            self.name: {
                "schema": self.name,
                "index": "all",
                "description": "NSAPH data model for gridMET climate data",
                "header": True,
                "quoting": 3,
                "tables": {
                }
            }
        }
        for geography in Geography:
            for band in GridmetVariable:
                bnd = band.value
                geo = geography.value
                date_column = "observation_date"
                tname = "{}_{}".format(geo, bnd)
                columns = [
                    {bnd: {
                        "type": PG_NUMERIC_TYPE
                    }},
                    {date_column: {
                        "type": PG_DATE_TYPE,
                        "source": "date"
                    }},
                    {geo: {
                        "type": PG_STR_TYPE
                    }}
                ]
                common_columns = yaml.safe_load(self.COMMON_COLUMNS)
                columns.extend(common_columns)
                if geography == Geography.county:
                    county_columns = yaml.safe_load(self.COUNTY_COLUMNS)
                    columns.extend(county_columns)
                elif geography == Geography.zcta:
                    zcta_columns = yaml.safe_load(self.ZCTA_COLUMNS)
                    columns.extend(zcta_columns)
                table = {
                    "columns": columns,
                    "primary_key": [
                        geo,
                        date_column
                    ],
                    "indices": {
                        "dt_geo_idx": {
                            "columns": [date_column, geo]
                        },
                        "ym_idx": {
                            "columns": ["year", "month"]
                        },
                        "y_geo_idx": {
                            "columns": ["year", geo]
                        }
                    }
                }
                domain[self.name]["tables"][tname] = table

        return yaml.dump(domain)

    @staticmethod
    def built_in_registry_path():
        src = Path(__file__).parents[3]
        return os.path.join(src, "yml", "gridmet.yaml")


if __name__ == '__main__':
    if len(sys.argv) > 2:
        dname = sys.argv[2]
    else:
        dname = None
    Registry(sys.argv[1], dname).update()
    