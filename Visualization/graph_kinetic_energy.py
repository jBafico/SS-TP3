from typing import List, Dict

from matplotlib.ticker import ScalarFormatter

from classes import Particle, SimulationSnapshot, SimulationOutput
from calculate_pressure import calculate_pressure_in_wall, PressureDataInInterval
import matplotlib.pyplot as plt


def get_system_kinetic_energy(simulations: List[SimulationSnapshot]) -> float:
    """
    Calculate the kinetic energy of the system.

    Parameters
    ----------
    simulations : list
        A list of SimulationSnapshot objects.

    Returns
    -------
    float
        The kinetic energy of the system.
    """
    particles = simulations[0].particles  # All snapshots will have the same kinetic energy, since the system is closed
    kinetic_energy = 0
    for particle in particles:
        particle_speed = (particle.vx ** 2 + particle.vy ** 2) ** 0.5
        kinetic_energy += 0.5 * particle.mass * particle_speed**2
    return kinetic_energy


def plot_pressure_by_kinetic_energy_for_simulations(simulation_outputs: List[SimulationOutput]) -> None:
    """
    Plot the pressure over time for all simulations.

    Parameters
    ----------
    simulation_outputs : List[SimulationOutput]
        A list of SimulationOutput objects.
    """
    pressure_by_kinetic_energy_dict: Dict[float, float] = {}
    kinetic_energy_to_velocity: Dict[float, float] = {}  # To store the initial velocity (v0) for each point

    for simulation_output in simulation_outputs:
        # Calculate avg kinetic energy of 3 repetitions
        kinetic_energy_by_repetition_number: Dict[str, float] = {}
        for simulation_name, simulations in simulation_output.simulations.items():
            kinetic_energy_by_repetition_number[simulation_name] = get_system_kinetic_energy(simulations)
        avg_kinetic_energy_for_all_repetitions = sum(kinetic_energy_by_repetition_number.values()) / len(kinetic_energy_by_repetition_number)

        # Calculate avg pressure of 3 repetitions
        pressure_in_timesteps_by_repetition_number: Dict[str, Dict[float, PressureDataInInterval]] = {}
        for simulation_name, simulations in simulation_output.simulations.items():
            final_time = simulations[-1].collision_event.time
            time_interval = final_time / 15
            pressure_in_timesteps_by_repetition_number[simulation_name] = calculate_pressure_in_wall(simulations, simulation_output.global_params.wall_radius, simulation_output.global_params.particle_mass, time_interval)
        avg_pressure_per_repetition = {
            simulation_name: sum(pressure_data.pressure for pressure_data in pressure_data_by_interval.values()) / len(pressure_data_by_interval)
            for simulation_name, pressure_data_by_interval in pressure_in_timesteps_by_repetition_number.items()
        }
        avg_pressure_for_all_repetitions = sum(avg_pressure_per_repetition.values()) / len(avg_pressure_per_repetition)

        # Store the pressure by kinetic energy and keep track of initial velocity
        pressure_by_kinetic_energy_dict[avg_kinetic_energy_for_all_repetitions] = avg_pressure_for_all_repetitions
        kinetic_energy_to_velocity[avg_kinetic_energy_for_all_repetitions] = simulation_output.global_params.velocity_modulus  # Store initial velocity

    # Plot the pressure by kinetic energy
    kinetic_energies = list(pressure_by_kinetic_energy_dict.keys())
    pressures = list(pressure_by_kinetic_energy_dict.values())  # Keep the pressures in their original units

    plt.figure(figsize=(8, 6))
    plt.scatter(kinetic_energies, pressures, color='blue')
    plt.plot(kinetic_energies, pressures, color='blue', linestyle='--')

    # Annotate each point with the corresponding initial velocity
    for kinetic_energy, pressure in zip(kinetic_energies, pressures):
        initial_velocity = kinetic_energy_to_velocity[kinetic_energy]
        plt.annotate(f'v₀ = {initial_velocity}\n', (kinetic_energy, pressure), textcoords="offset points", xytext=(5, 10), ha='center')

    # Set scientific notation for the x-axis with superscript
    ax = plt.gca()
    # X-axis formatting
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))
    # Y-axis formatting
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    # Set axis labels and grid
    plt.xlabel('Energia Cinetica (J)')
    plt.ylabel('Presión (N/m)')
    plt.grid(True)

    # Format the Y-axis to show values in scientific notation
    plt.ticklabel_format(style='scientific', axis='y', scilimits=(0, 0))

    plt.tight_layout()
    plt.show()
