from typing import List, Dict
from dataclasses import dataclass
import matplotlib.pyplot as plt
from math import pi

from Visualization.classes import SimulationOutput, Particle


@dataclass
class PressureDataInInterval:
    interval_start: float
    interval_end: float
    pressure: float = 0
    momentum_sum: float = 0
    total_wall_collisions: int = 0

    def __str__(self):
        return f"PressureDataInInterval(interval_start={self.interval_start}, interval_end={self.interval_end}, pressure={self.pressure}, momentum_sum={self.momentum_sum}, total_wall_collisions={self.total_wall_collisions})"


def plot_pressure_over_time(simulation_output: SimulationOutput) -> None:
    # Calculate the pressure data by time intervals
    pressure_data_by_interval: Dict[float, PressureDataInInterval] = calculate_pressure(simulation_output)

    # Extract time intervals and corresponding pressures
    time_intervals = []
    pressures = []

    for interval_end, pressure_data in sorted(pressure_data_by_interval.items()):
        time_intervals.append(pressure_data.interval_end)
        pressures.append(pressure_data.pressure)

    # Plot the pressure vs time
    plt.figure(figsize=(10, 6))
    plt.plot(time_intervals, pressures, marker='o', linestyle='-', color='b')

    # Add labels and title
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Presión (N/m)')
    plt.grid(True)
    plt.legend()

    # Ensure the Y-axis starts from 0
    plt.ylim(bottom=0)

    # Show the plot
    plt.show()


def calculate_pressure(simulation_output: SimulationOutput) -> Dict[float, PressureDataInInterval]:
    circle_radius = simulation_output.global_params.wall_radius

    final_time = simulation_output.simulations[-1].collision_event.time
    time_interval = final_time / 15

    # The key of the dict is the end of the time interval
    pressure_data_by_interval: Dict[float, PressureDataInInterval] = {}
    for simulation in simulation_output.simulations:
        # We are only interested in wall collisions
        if simulation.collision_event.collision_type != "wall":
            continue

        # Calculate the normal velocity to the wall and get the particle mass
        vn = calculate_normal_velocity_to_wall(simulation.collision_event.particle1)
        particle_mass = simulation_output.global_params.particle_mass

        # Generate the corresponding dict key
        time_interval_end = simulation.collision_event.time // time_interval * time_interval + time_interval

        # Get or create interval info
        pressure_data_in_interval = pressure_data_by_interval.get(time_interval_end, PressureDataInInterval(interval_start=time_interval_end - time_interval, interval_end=time_interval_end))

        # Update interval info
        pressure_data_in_interval.momentum_sum += 2 * particle_mass * vn
        pressure_data_in_interval.total_wall_collisions += 1
        pressure_data_in_interval.pressure = pressure_data_in_interval.momentum_sum / (2*pi*circle_radius * time_interval)
        pressure_data_by_interval[time_interval_end] = pressure_data_in_interval

    return pressure_data_by_interval


def calculate_normal_velocity_to_wall(particle: Particle) -> float:
    """Calculate the normal velocity of a particle to a wall"""
    # Calculate distance from particle center to center
    distance = (particle.x ** 2 + particle.y ** 2) ** 0.5

    # Calculate the normal versor to the wall
    nx = particle.x / distance
    ny = particle.y / distance

    # Calculate the normal velocity to the wall
    vn = particle.vx * nx + particle.vy * ny

    return vn

