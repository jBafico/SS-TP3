import os
from parse_json_simulation import parse_json_simulation
from load_most_recent_json import load_most_recent_simulation_json
from classes import SimulationOutput, SimulationSnapshot
import json
import matplotlib.pyplot as plt

import numpy as np

import matplotlib.ticker as mticker


output_dir = "item3Output"


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



def reduce_items(collision_dict):

    x_values = []
    y_values = []

    total_collisions = 0
    for time, collisionQty in collision_dict.items():
        x_values.append(time)
        total_collisions += collisionQty
        y_values.append(total_collisions)

    return x_values, y_values


def render_collision_graph(collision_dict: list[dict[float, int]],countOnlyOnce: bool, dataVelocitys):
    # Create the directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)


    min_y_value = float('inf')

    for current_collision_dict,color, velocity in zip(collision_dict,["red","green","blue","purple"], dataVelocitys):
        x_values , y_values = reduce_items(current_collision_dict)

        current_min = min(y_values)
        if current_min < min_y_value:
            min_y_value = current_min


        # Create scatter plot
        plt.scatter(x_values, y_values, color=color)

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
    plt.ylim(0, min_y_value)

    # Save the plot to a file in the output directory
    output_file = os.path.join(output_dir, f"collision_graph_countOnlyOnce_{countOnlyOnce}_.png")
    plt.savefig(output_file)

    plt.clf()

    print(f"Graph saved to {output_file}")

def get_simulation_last_time(simulation_data : SimulationOutput):
    return simulation_data.simulations[-1].collision_event.time



def reduce_to_stationary_period_threshold(x_values: np.ndarray, y_values: np.ndarray, threshold: float, n: int) -> float:
    """
    Detect the first x-coordinate where the stationary period begins based on consecutive y-values being within a given threshold.

    :param x_values: An array of x coordinates.
    :param y_values: An array of y coordinates.
    :param threshold: The maximum allowed difference between consecutive y-values to consider them stationary.
    :param n: The number of consecutive points that must meet the threshold.
    :return: The x-coordinate where the stationary period starts, or None if not found.
    """
    # Count the number of consecutive values that are within the threshold
    consecutive_count = 0
    
    for i in range(1, len(y_values)):
        # Check if the difference between consecutive y-values is within the threshold
        if abs(y_values[i] - y_values[i - 1]) <= threshold:
            consecutive_count += 1
        else:
            consecutive_count = 0  # Reset if the difference exceeds the threshold
        
        # If we've found n consecutive points within the threshold, return the first x-coordinate
        if consecutive_count >= n:
            return x_values[i - n + 1]  # Return the x-value where stationarity starts
    
    raise Exception("NO STATIONARY PERIOD WAS FOUND")
    

def create_collision_graph_data(simulations: list[SimulationSnapshot] ,config, ):

    #Diccionario mapea tiempo de colision => cantidad de colisiones
    collisionDic : dict[float, int] = {} 

    already_collisioned = set()
    for simulation in simulations:
        
        if simulation.collision_event.collision_type == "wall": # Si es pared no me interesa
            continue
        if simulation.collision_event.particle1.id != 0 and simulation.collision_event.particle2.id != 0: # Si no esta involucrado el objeto quieto no me interesa
            continue

        otherParticle = simulation.collision_event.particle1
        if simulation.collision_event.particle1.id == 0: # Era la otra
            otherParticle = simulation.collision_event.particle2

        if config["countColisionOnlyOnce"]:
            if otherParticle.id in already_collisioned:
                collisionDic[simulation.collision_event.time] = 0
                continue
            already_collisioned.add(otherParticle.id)

        collisionDic[simulation.collision_event.time] = collisionDic.get(simulation.collision_event.time, 0) + 1

    return collisionDic


    
def reduce_to_slope(x_values , y_values) -> float:
    # Ensure inputs are NumPy arrays
    x = np.array(x_values)
    y = np.array(y_values)
    
    # Number of points
    n = len(x)
    
    # Calculate the components of the slope formula
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_xy = np.sum(x * y)
    sum_x_squared = np.sum(x ** 2)
    
    # Calculate the slope (m)
    slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
    
    return slope


def create_observables_graphics(simulation_data : list[SimulationOutput], config):
    
    #Mapeo velocidad => lista de observables para esa velocidad
    velocities_to_slopes : dict[float, list[float]] =  {}
    for simulation_for_given_velocitiy in simulation_data:
        observables_list = []
        for current_simulation_list in simulation_for_given_velocitiy.simulations.values():
            data : dict[float,int] = create_collision_graph_data(current_simulation_list,config)
            x_values, y_values = reduce_items(data)
            current_observable = None
            if config["countColisionOnlyOnce"]:
                current_observable = reduce_to_stationary_period_threshold(x_values,y_values,config["stationaryThresholdTolerance"],config["stationaryThresholdPeriods"])
            else:
                current_observable = reduce_to_slope(x_values,y_values)
            observables_list.append(current_observable)
        velocities_to_slopes[simulation_for_given_velocitiy.global_params.velocity_modulus] = observables_list

    plot_scatter_with_error_bars(velocities_to_slopes,config)



def plot_scatter_with_error_bars(velocities_to_slopes: dict[float, list[float]],config):
    # Extract keys (velocities) and corresponding values (list of slopes)
    velocities = np.array([x**2 for x in velocities_to_slopes.keys()])
    means = np.array([np.mean(slopes) for slopes in velocities_to_slopes.values()])
    std_devs = np.array([np.std(slopes) for slopes in velocities_to_slopes.values()])
    
    # Create a scatter plot with error bars
    plt.errorbar(velocities, means, yerr=std_devs, fmt='o', capsize=5)

    # Add labels and title
    plt.xlabel('Velocidad (m\u00b2/s\u00b2)')
    plt.ylabel('Pendiente de recta')

    # Show legend
    plt.legend()


    
    # Save the plot to a file in the output directory
    output_name = "observables_onlyOnce.png" if config["countColisionOnlyOnce"] else "observables_notOnlyOnce.png"
    output_file = os.path.join(output_dir,output_name)
    plt.savefig(output_file)

    print(f"Graph observables saved to {output_file}")
    








if __name__ == "__main__":
    with open("./grapherItem3config.json","r") as f:
        config = json.load(f)
    json_data = load_most_recent_simulation_json("../files")
    simulation_data = parse_json_simulation(json_data)
    if config["renderOneGraph"]:
        dataList = []
        dataVelocitys = []
        for simulation in simulation_data:
            simulations = simulation.simulations["simulation_1"]
            data = create_collision_graph_data(simulations,config)
            dataList.append(data)
            dataVelocitys.append(simulation.global_params.velocity_modulus)
        
        render_collision_graph(dataList,config["countColisionOnlyOnce"], dataVelocitys)

    if config["graphicObservables"]:
        create_observables_graphics(simulation_data,config)


    print("FINISHED")






