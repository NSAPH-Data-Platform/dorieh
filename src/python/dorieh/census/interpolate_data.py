import pickle
import logging
from dorieh.utils.context import Context, Argument, Cardinality


class CensusInterpolateContext(Context):

    _interpolate = Argument("interpolate",
                            help="""Years to interpolate for. Takes min year + max year formatted 
                                as <min_year>:<max_year>. Enter 'x' to skip interpolation""",
                            aliases=["i"],
                            cardinality=Cardinality.single,
                            default="1999:2019",
                            )
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
                        default="census_interpolated.pkl"
                        )

    def __init__(self):
        self.interpolate = None
        self.log = None
        self.in_pkl = None
        self.out_pkl = None
        super().__init__(CensusInterpolateContext)

    def validate(self, attr, value):
        value = super().validate(attr, value)

        if attr == "interpolate":
            value = value.split(":")
            out = dict()
            out["min"] = int(value[0])
            out["max"] = int(value[1])
            return out

        return value


def initialize_logging(log: str):
    handler = logging.FileHandler(log, mode="a")
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger("dorieh.utils")
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return True


if __name__ == "__main__":
    context = CensusInterpolateContext().instantiate()
    initialize_logging(context.log)

    with open(context.in_pkl, 'rb') as f:
        census = pickle.load(f)

    census.interpolate(min_year=context.interpolate["min"], max_year=context.interpolate["max"])

    with open(context.out_pkl, 'wb') as f:
        pickle.dump(census, f)
