from load_most_recent_json import load_most_recent_simulation_json
from classes import *
from parse_json_simulation import parse_json_simulation


def main():
    print("Parsing JSON data...")

    # Load the most recent simulation JSON data
    json_data = load_most_recent_simulation_json('../files')
    simulation_output = parse_json_simulation(json_data)

    print("Finished parsing JSON data.")

    print("Plotting data...")


    print("Finished plotting data.")


if __name__ == '__main__':
    main()
