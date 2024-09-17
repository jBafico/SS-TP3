import json
import math

from matplotlib import pyplot as plt
import numpy as np
from classes import SimulationOutput, SimulationSnapshot
from load_most_recent_json import load_most_recent_simulation_json
from parse_json_simulation import parse_json_simulation
import os

output_dir = "item4Output"

def calculate_distance_to_center(prev_snapshot: SimulationSnapshot):
    big_particle = None
    for particle in prev_snapshot.particles:
        if particle.id == 0:
            big_particle = particle
            break
    
    distance = math.sqrt(big_particle.x ** 2 + big_particle.y ** 2)
    
    return distance


def obtain_mcd_graphic(simulation_data : SimulationOutput, config):
    print(find_max_time_in_all_simulation(simulation_data))
    start = config["dmcTimeStart"]
    end = config["dmcTimeEnd"]
    step = config["dcmStep"]
    current_time = start
    
    time_slices_data : dict[str, list[float]] = {}
    while current_time <= end:
        time_slices_data[str(current_time)] = []
        current_time += step

    for simulationSnapshots in simulation_data.simulations.values():
        current_time = step
        for i in range(1,len(simulationSnapshots)):
            if simulationSnapshots[i].collision_event.time > current_time:
                prev_snapshot = simulationSnapshots[i-1]
                distance = calculate_distance_to_center(prev_snapshot)
                time_slices_data[str(current_time)].append(distance)
                current_time += step

    toGraph_dict = {}
    for key,value in time_slices_data.items():
        if len(value) == len(simulation_data.simulations):
            toGraph_dict[float(key)] = value



    plot_scatter_with_error_bars(toGraph_dict)
            



def plot_scatter_with_error_bars(velocities_to_slopes: dict[float, list[float]]):
    # Extract keys (velocities) and corresponding values (list of slopes)
    velocities = np.array([x**2 for x in velocities_to_slopes.keys()])
    means = np.array([np.mean(slopes) for slopes in velocities_to_slopes.values()])
    std_devs = np.array([np.std(slopes) for slopes in velocities_to_slopes.values()])
    
    # Create a scatter plot with error bars
    plt.errorbar(velocities, means, yerr=std_devs, fmt='o', capsize=5)

    # Add labels and title
    plt.xlabel('Tiempo (s)')
    plt.ylabel('DCM (m)')

    # Show legend
    plt.legend()


    
    # Save the plot to a file in the output directory
    output_name = "observables_mcd.png"
    output_file = os.path.join(output_dir,output_name)
    os.makedirs(output_dir, exist_ok=True)

    plt.savefig(output_file)

    print(f"Graph observables saved to {output_file}")
    


        


def find_max_time_in_all_simulation(simulation_data: SimulationOutput):
    max_time = -1
    simulations = simulation_data.simulations
    for simulation in simulations.values():
        current_time = simulation[-1].collision_event.time
        if current_time >= max_time:
            max_time = current_time

    print("Max time",max_time)

    return max_time




if __name__ == "__main__":
    with open("./grapherItem4config.json","r") as f:
        config = json.load(f)
     
    json_data = load_most_recent_simulation_json("../files")
    simulation_data = parse_json_simulation(json_data)
    obtain_mcd_graphic(simulation_data[0], config)
    print("FINISHED")

