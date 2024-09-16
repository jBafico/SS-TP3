from parse_json_simulation import parse_json_simulation
from load_most_recent_json import load_most_recent_simulation_json
from classes import SimulationOutput
import json
import matplotlib.pyplot as plt

import numpy as np

import matplotlib.ticker as mticker

def scientific_to_superscript(sci_string):
    # Map for superscript digits and the minus sign
    superscript_map = {
        '0': '⁰',
        '1': '¹',
        '2': '²',
        '3': '³',
        '4': '⁴',
        '5': '⁵',
        '6': '⁶',
        '7': '⁷',
        '8': '⁸',
        '9': '⁹',
        '-': '⁻'
    }
    
    # Split the string into base and exponent parts (assuming 'e' format)
    base, exp = sci_string.split('e')

    # Convert exponent into superscript characters
    exp_superscript = ''.join(superscript_map.get(char, char) for char in exp)
    
    # Return the formatted string with superscript exponent
    return f"{base}×10{exp_superscript}"

def render_collision_graph(collision_dict: dict[float, dict[int, int]]):
    x_values = []
    y_values = []

    for x, sub_dict in collision_dict.items():
        x_values.append(x)
        y_values.append(sum(sub_dict.values()))

    # Create scatter plot
    plt.scatter(x_values, y_values)

    # Add a line connecting the scatter points
    plt.plot(x_values, y_values, linestyle='-', color='blue')

    plt.xlabel("Intervalo")
    plt.ylabel("Nro Choques")
    
    # Display only the x-values on the x-axis
    plt.xticks(x_values)
    
    # Display only integer values on the y-axis
    plt.yticks(np.arange(min(y_values), max(y_values) + 1, step=1))  # Set y-axis ticks to integers
    
    # Use scientific notation for each x-tick
    formatter = mticker.FuncFormatter(lambda x, _: scientific_to_superscript(f'{x:.2e}'))# GRANDE RANITA!!!
    plt.gca().xaxis.set_major_formatter(formatter)

    plt.legend()
    plt.show()



def get_simulation_last_time(simulation_data : SimulationOutput):
    return simulation_data.simulations[-1].collision_event.time



    

def create_collision_graph(simulation_data: SimulationOutput,config):
    lastTime = get_simulation_last_time(simulation_data)
    slot = lastTime / config["timeSlotDivision"]

    simulations = simulation_data.simulations
    current_time = slot

    #Diccionario mapea tiempo de colision => id particula => cantidad de veces que colisiono
    collisionDic : dict[float, dict[int,int]] = {} 
    collisionDic.setdefault(current_time, {})
    for simulation in simulations:
        if simulation.collision_event.time > current_time:
            current_time += slot
            collisionDic.setdefault(current_time, {})

        if simulation.collision_event.collision_type == "wall": # Si es pared no me interesa
            continue
        if simulation.collision_event.particle1['id'] != 0 and simulation.collision_event.particle2['id'] != 0: # Si no esta involucrado el objeto quieto no me interesa
            continue

        otherParticle = simulation.collision_event.particle1
        if simulation.collision_event.particle1['id'] == 0: #Era la otra
            otherParticle = simulation.collision_event.particle2

        if config["countColisionOnlyOnce"]:
            collisionDic[current_time][otherParticle['id']] = 1
        else: # Initialize with 1 if the key doesn't exist, otherwise add 1 to the current value
            collisionDic[current_time][otherParticle['id']] = collisionDic[current_time].get(otherParticle['id'], 0) + 1


    render_collision_graph(collisionDic)











if __name__ == "__main__":
    with open("./grapherItem3config.json","r") as f:
        config = json.load(f)
    json_data = load_most_recent_simulation_json("../files")
    simulation_data = parse_json_simulation(json_data)
    create_collision_graph(simulation_data,config)






