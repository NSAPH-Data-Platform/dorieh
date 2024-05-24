import logging
import pickle
from dorieh.utils.context import Context, Argument, Cardinality


class CensusQCContext(Context):

    _log = Argument("log",
                    help="Path to log file",
                    cardinality=Cardinality.single,
                    default="cwl_census.log")
    _in_pkl = Argument("in_pkl",
                       help="Path to temporary input pkl file",
                       cardinality=Cardinality.single,
                       default="census.pkl")
    _qc_file = Argument("qc_file",
                        help="Path to QC file",
                        cardinality = Cardinality.single,
                        default = "qc.yml")
    _qc_log = Argument("qc_log",
                    help="Path to QC log file",
                    cardinality=Cardinality.single,
                    default="cwl_census_qc.log")

    def __init__(self):
        self.log = None
        self.in_pkl = None
        self.qc_file = None
        self.qc_log = None

        super().__init__(CensusQCContext)


def initialize_logging(log: str, qc_log: str):
    handler = logging.FileHandler(log, mode="a")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger("")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    qc_handler = logging.FileHandler(qc_log, mode="w")
    qc_formatter = logging.Formatter('%(levelname)s - %(name)s - %(message)s - %(asctime)s')
    qc_handler.setFormatter(qc_formatter)

    qc_logger = logging.getLogger("dorieh.utils.qc")
    qc_logger.addHandler(qc_handler)
    qc_logger.setLevel(logging.DEBUG)

    return True


if __name__ == "__main__":
    context = CensusQCContext().instantiate()
    initialize_logging(context.log, context.qc_log)

    with open(context.in_pkl, 'rb') as f:
        census = pickle.load(f)

    census.quality_check(context.qc_file)
