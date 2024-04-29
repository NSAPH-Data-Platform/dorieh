import logging
import pickle
from dorieh.utils.context import Context, Argument, Cardinality


class CensusDensityContext(Context):
    _log = Argument("log",
                    help="Path to log file",
                    cardinality=Cardinality.single,
                    default="cwl_census.log")
    _in_pkl = Argument("in_pkl",
                       help="Path to temporary input pkl file",
                       cardinality=Cardinality.single,
                       default="census.pkl")
    _out_pkl = Argument("out_pkl",
                        help="Path to temporary output pkl file",
                        cardinality=Cardinality.single,
                        default="census_density.pkl"
                        )
    _densities = Argument("densities",
                          aliases=['d'],
                          help="""Names of variables to calculate denisity per square mile for. If ommitted, 
                                  density calculation will be skipped. To calculate population density, assuming
                                  population is stored in a variable named 'population', the option would be specified
                                  -d population""",
                          cardinality=Cardinality.multiple,
                          default=None,
                          required=False)

    def __init__(self):
        self.log = None
        self.in_pkl = None
        self.out_pkl = None
        self.densities = None

        super().__init__(CensusDensityContext)


def initialize_logging(log: str):
    handler = logging.FileHandler(log, mode="a")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger("get_census")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


if __name__ == "__main__":

    context = CensusDensityContext().instantiate()
    initialize_logging(context.log)

    with open(context.in_pkl, 'rb') as f:
        census = pickle.load(f)

    census.calculate_densities(context.densities)

    with open(context.out_pkl, 'wb') as f:
        pickle.dump(census, f)
