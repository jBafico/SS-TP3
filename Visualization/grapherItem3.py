import os
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


def render_collision_graph(collision_dict: dict[float, int],countOnlyOnce: bool):
    # Create the directory if it doesn't exist
    output_dir = "item3Output"
    os.makedirs(output_dir, exist_ok=True)
    
    x_values = []
    y_values = []

    total_collisions = 0
    for time, collisionQty in collision_dict.items():
        x_values.append(time)
        total_collisions += collisionQty
        y_values.append(total_collisions)

    # Create scatter plot
    plt.scatter(x_values, y_values)

    # Add a line connecting the scatter points
    plt.plot(x_values, y_values, linestyle='-', color='blue')

    plt.xlabel("Tiempo (s)")
    plt.ylabel("Nro Choques")
    
    # Display only the x-values on the x-axis
    plt.xticks(fontsize=12)
    
    # Display only integer values on the y-axis
    plt.yticks(fontsize=12)
    
    # Use scientific notation for each x-tick
    plt.gca().xaxis.set_major_formatter(mticker.ScalarFormatter(useMathText=True))
    plt.gca().ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    
    # Set the y-axis limit to allow space above the maximum value
    max_y_value = max(y_values)
    plt.ylim(0, max_y_value * 1.1)

    # Save the plot to a file in the output directory
    output_file = os.path.join(output_dir, f"collision_graph_countOnlyOnce_{countOnlyOnce}.png")
    plt.savefig(output_file)

    print(f"Graph saved to {output_file}")

def get_simulation_last_time(simulation_data : SimulationOutput):
    return simulation_data.simulations[-1].collision_event.time



    

def create_collision_graph(simulation_data: SimulationOutput,config):

    simulations = simulation_data.simulations["simulation_1"]

    #Diccionario mapea tiempo de colision => cantidad de colisiones
    collisionDic : dict[float, int] = {} 

    already_collisioned = set()
    for simulation in simulations:
        
        if simulation.collision_event.collision_type == "wall": # Si es pared no me interesa
            continue
        if simulation.collision_event.particle1['id'] != 0 and simulation.collision_event.particle2['id'] != 0: # Si no esta involucrado el objeto quieto no me interesa
            continue

        otherParticle = simulation.collision_event.particle1
        if simulation.collision_event.particle1['id'] == 0: #Era la otra
            otherParticle = simulation.collision_event.particle2

        if config["countColisionOnlyOnce"]:
            if otherParticle['id'] in already_collisioned:
                collisionDic[simulation.collision_event.time] = 0
                continue
            already_collisioned.add(otherParticle['id'])

        collisionDic[simulation.collision_event.time] = collisionDic.get(simulation.collision_event.time,0) + 1


    render_collision_graph(collisionDic,config["countColisionOnlyOnce"])











if __name__ == "__main__":
    with open("./grapherItem3config.json","r") as f:
        config = json.load(f)
    json_data = load_most_recent_simulation_json("../files")
    simulation_data = parse_json_simulation(json_data)
    create_collision_graph(simulation_data,config)






