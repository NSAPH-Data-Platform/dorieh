import argparse
import csv
import logging
from typing import List, Optional

from dorieh.epa import PARAMETER_CODE, MONITOR, RECORD
from dorieh.epa.aqs_ds_def import Parameter
from dorieh.epa.aqs_tools import transfer
from dorieh.platform import init_logging
from dorieh.utils.io_utils import fopen, file_as_csv_reader

log = logging.getLogger(__name__)

TARGET = "output.csv.gz"


def expand_data(files: List[str], parameter: Optional[int]) -> str:
    log.info("Expand files %r with parameter %r", files, parameter)

    write_header = True
    for filename in files:
        log.info("Process %s", filename)

        with fopen(TARGET, "at") as ostream:
            reader = file_as_csv_reader(filename)

            fieldnames = list(reader.fieldnames)
            fieldnames.append(MONITOR)
            fieldnames.append(RECORD)
            writer = csv.DictWriter(ostream, fieldnames, quotechar='"',
                                    delimiter=',',
                                    quoting=csv.QUOTE_NONNUMERIC)
            if parameter:
                flt = lambda row: int(row[PARAMETER_CODE]) == parameter
            else:
                flt = None
            transfer(reader, writer, flt, write_header)
            write_header = False

    return TARGET


if __name__ == '__main__':
    init_logging()
    ap = argparse.ArgumentParser()
    ap.add_argument("--parameter_code", dest="parameter", type=str, required=False, help="Parameter")
    ap.add_argument('files', type=str, nargs='+', help='files to parse')
    args = ap.parse_args()

    try:
        parameter = Parameter.validate(args.parameter)
    except ValueError:
        print("Unknown parameter ", args.parameter)
        exit(1)

    expand_data(files=args.files, parameter=parameter)
