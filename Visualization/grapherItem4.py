import json
import math

from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
import numpy as np
from classes import SimulationOutput, SimulationSnapshot
from load_most_recent_json import load_most_recent_simulation_json
from parse_json_simulation import parse_json_simulation
import os

output_dir = "item4Output"
TRIES = 720

def SuperScriptinate(number):
  return number.replace('0','⁰').replace('1','¹').replace('2','²').replace('3','³').replace('4','⁴').replace('5','⁵').replace('6','⁶').replace('7','⁷').replace('8','⁸').replace('9','⁹').replace('-','⁻')

def sci_notation(number, sig_fig=2):
    ret_string = "{0:.{1:d}e}".format(number, sig_fig)
    a,b = ret_string.split("e")
    b = int(b)         # removed leading "+" and strips leading zeros too.
    return a + "x10" + SuperScriptinate(str(b))

def calculate_distance_to_center(prev_snapshot: SimulationSnapshot):
    big_particle = None
    for particle in prev_snapshot.particles:
        if particle.id == 0:
            big_particle = particle
            break
    
    distance = math.sqrt(big_particle.x ** 2 + big_particle.y ** 2) ** 2
    
    return distance


def obtain_mcd_graphic(simulation_data : SimulationOutput, config):
    print(find_max_time_in_all_simulation(simulation_data))
    start = config["dmcTimeStart"]
    end = config["dmcTimeEnd"]
    step = config["dcmStep"]
    current_time = start
    
    time_slices_data : dict[str, list[float]] = {}
   
    for simulationSnapshots in simulation_data.simulations.values():
        current_time = step
        for i in range(1,len(simulationSnapshots)):
            if simulationSnapshots[i].collision_event.time > current_time:
                prev_snapshot = simulationSnapshots[i-1]
                distance = calculate_distance_to_center(prev_snapshot)
                if str(current_time) not in time_slices_data:
                    time_slices_data[str(current_time)] = []
                time_slices_data[str(current_time)].append(distance)
                current_time += step

    toGraph_dict = {}
    for key,value in time_slices_data.items():
        if len(value) == len(simulation_data.simulations):
            toGraph_dict[float(key)] = value

    plot_scatter_with_error_bars(toGraph_dict)





def reduce_to_slope(xs, ys):
    Y_INTERCEPT = 0
    LINEAR_FUNCTION = lambda x, m: m * x + Y_INTERCEPT

    candidate_slope = 0
    min_error = np.inf

    max_slope = max(ys) / max(xs)
    slopes = np.arange(0, max_slope, max_slope / TRIES)



    xs_out = []
    ys_out = []
    for slope in slopes:
        d = slope / 4
        error = 0
        for x, y in zip(xs, ys):
            error += (y - LINEAR_FUNCTION(x, slope))**2
        if error < min_error:
            min_error = error
            candidate_slope = slope
        xs_out.append(d)
        ys_out.append(error)

    return candidate_slope, min_error , xs_out, ys_out



def plot_scatter_with_error_bars(time_to_dmc: dict[float, list[float]]):
    output_dict = {}
    # Extract keys (velocities) and corresponding values (list of slopes)
    time = np.array(list(time_to_dmc.keys()))
    means = np.array([np.mean(slopes) for slopes in time_to_dmc.values()])
    std_devs = np.array([np.std(slopes) for slopes in time_to_dmc.values()])

    # Create a scatter plot with error bars
    plt.errorbar(time, means, yerr=std_devs, fmt='o', capsize=5)

    slope, minError ,xs_out, ys_out = reduce_to_slope(time, means)
    output_dict["minError"] = minError
    output_dict["bestSlope"] = slope
    output_dict["defusionCoeficient"] = slope / 4

    # Set scientific notation for the x-axis with superscript
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    # Y-axis formatting
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    # Add labels and title
    plt.xlabel('Tiempo (s)')
    plt.ylabel('DCM (m\u00b2)')

    # Show legend   
    plt.legend()

    # Save the plot to a file in the output directory
    output_name = "observables_mcd.png"
    output_file = os.path.join(output_dir, output_name)
    os.makedirs(output_dir, exist_ok=True)

    plt.savefig(output_file)
    print(f"Graph observables saved to {output_file}")

    # Plot the linear function (y = slope * time) in red
    linear_fit = slope * time  # Linear function with calculated slope
    print("SLOPE",f"{slope}")
    plt.plot(time, linear_fit, 'r-', label=f'Recta de ajuste (y={sci_notation(slope)} t)')
    plt.legend()

    # Save the plot to a file in the output directory
    output_name = "observables_with_slope_mcd.png"
    output_file = os.path.join(output_dir, output_name)
    os.makedirs(output_dir, exist_ok=True)

    plt.savefig(output_file)
    plt.clf()


    ax = plt.gca()
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    # Y-axis formatting
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    plt.scatter(x=xs_out, y=ys_out)
    plt.xlabel("D (m\u00b2/s)")
    plt.ylabel("Error (m\u00b2)")
    
    plt.axvline(x=slope / 4, color='r', linestyle='--',label=f"Error={sci_notation(minError)} Coeficiente Defusion = {sci_notation(slope / 4)}")
    plt.legend()

    output_name = "observables_with_cuadratic.png"
    output_file = os.path.join(output_dir, output_name)
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_file)
    plt.close()


    with open('./item4Output/data.json', 'w') as json_file:
        json.dump(output_dict, json_file, indent=4)

    




        


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

