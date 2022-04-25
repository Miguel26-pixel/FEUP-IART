import sys
from meta.annealing import run_annealing
from meta.genetic import run_genetic

from utils.parser import setup_parser, parse_information

if __name__ == "__main__":
    parser = setup_parser()
    parsed = parser.parse_args(sys.argv[1:])

    if parsed.problem == "paris":
        print("Reading Paris problem")
        router = parse_information('../files/input2.txt')
    elif parsed.problem == "random":

        pass
    else:
        print("Wrong format of problem")
        exit(1)

    if parsed.annealing:
        print("Running simulated annealing")
        run_annealing(router, parsed)
    elif parsed.genetic:
        run_genetic(router, parsed)
    else:
        print("Nothing to do...")
