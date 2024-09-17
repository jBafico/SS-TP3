import json
import math
from classes import SimulationOutput, SimulationSnapshot
from load_most_recent_json import load_most_recent_simulation_json
from parse_json_simulation import parse_json_simulation

DCM_SLICE_KEY = "dcmTimeSlice"


def calculate_distance_to_center(prev_snapshot: SimulationSnapshot):
    big_particle = None
    for particle in prev_snapshot.particles:
        if particle.id == 0:
            big_particle = particle
            break
    
    distance = math.sqrt(big_particle.x ** 2 + big_particle.y ** 2)
    
    return distance


def obtain_mcd_graphic(simulation_data : SimulationOutput, config):
    max_time = find_max_time_in_all_simulation(simulation_data)
    print("max_time",max_time)
    time_slice = max_time / config[DCM_SLICE_KEY]
    current_time = time_slice
    
    time_slices_data : dict[str, list[float]] = {}
    while current_time <= max_time:
        time_slices_data[str(current_time)] = []
        current_time += time_slice

    for simulationSnapshots in simulation_data.simulations.values():
        current_time = time_slice
        for i in range(1,len(simulationSnapshots)):
            if simulationSnapshots[i].collision_event.time >= current_time:
                prev_snapshot = simulationSnapshots[i-1]
                distance = calculate_distance_to_center(prev_snapshot)
                time_slices_data[str(current_time)].append(distance)
                current_time += time_slice
        time_slices_data[str(max_time)].append(calculate_distance_to_center(simulationSnapshots[-1]))

    print("")
            

        


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

