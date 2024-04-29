import pickle
import logging
from dorieh.utils.context import Context, Argument, Cardinality


class CensusWriteContext(Context):
    _in_pkl = Argument("in_pkl",
                       help="Path to temporary input pkl file",
                       cardinality=Cardinality.single,
                       default="census.pkl")
    _out_file = Argument("out_file",
                         aliases=["out"],
                         help="name of file to write output to",
                         cardinality=Cardinality.single,
                         default=None)
    _schema_name = Argument("schema_name",
                            help="name to write schema file to",
                            cardinality=Cardinality.single,
                            default=None,
                            required=False)
    _log = Argument("log",
                    help="Path to log file",
                    cardinality=Cardinality.single,
                    default="cwl_census.log")
    _table_name = Argument("table_name",
                           help="name for the table in the database",
                           cardinality=Cardinality.single,
                           default = None,
                           required=False)

    def __init__(self):
        self.in_pkl = None
        self.out_file = None
        self.schema_name = None
        self.log = None
        self.table_name = None
        super().__init__(CensusWriteContext)


def initialize_logging(log: str):
    handler = logging.FileHandler(log, mode="a")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger("get_census")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


if __name__ == "__main__":

    context = CensusWriteContext().instantiate()
    initialize_logging(context.log)

    with open(context.in_pkl, 'rb') as f:
        census = pickle.load(f)

    census.write_schema(context.schema_name, context.table_name)
    census.write_data(context.out_file)
