from typing import List, Dict
from dataclasses import dataclass
import matplotlib.pyplot as plt
from math import pi

from matplotlib.ticker import ScalarFormatter

from Visualization.classes import Particle, SimulationSnapshot


@dataclass
class PressureDataInInterval:
    interval_start: float
    interval_end: float
    pressure: float = 0
    momentum_sum: float = 0
    total_collisions: int = 0

    def __str__(self):
        return f"PressureDataInInterval(interval_start={self.interval_start}, interval_end={self.interval_end}, pressure={self.pressure}, momentum_sum={self.momentum_sum}, total_wall_collisions={self.total_collisions})"


def plot_pressure_over_time(simulation_snapshots: List[SimulationSnapshot], circle_radius: float, center_particle_radius: float, particle_mass: float, v0: float) -> None:
    # Calculate the time interval for the pressure data
    final_time = simulation_snapshots[-1].collision_event.time
    time_interval = final_time / 15

    # Calculate the pressure data by time intervals
    pressure_in_wall: Dict[float, PressureDataInInterval] = calculate_pressure_in_wall(simulation_snapshots, circle_radius, particle_mass, time_interval)
    pressure_in_center_particle: Dict[float, PressureDataInInterval] = calculate_pressure_in_center_particle(simulation_snapshots, center_particle_radius, particle_mass, time_interval)

    # Extract time intervals and corresponding pressures
    time_intervals = []
    pressures_in_wall = []
    pressures_in_center_particle = []

    for interval_end, pressure_data in sorted(pressure_in_wall.items()):
        time_intervals.append(pressure_data.interval_end)
        pressures_in_wall.append(pressure_data.pressure)

    for interval_end, pressure_data in sorted(pressure_in_center_particle.items()):
        pressures_in_center_particle.append(pressure_data.pressure)

    # Remove the last value of the time intervals, since they are outliers
    time_intervals.pop()
    pressures_in_wall.pop()
    pressures_in_center_particle.pop()

    # Calculate mean pressures
    mean_wall_pressure = sum(pressures_in_wall) / len(pressures_in_wall) if pressures_in_wall else 0
    mean_center_pressure = sum(pressures_in_center_particle) / len(pressures_in_center_particle) if pressures_in_center_particle else 0

    # Plot the pressure vs time
    plt.figure(figsize=(10, 6))
    plt.plot(time_intervals, pressures_in_wall, marker='o', linestyle='-', color='b', label='Presión en la pared')
    plt.plot(time_intervals, pressures_in_center_particle, marker='o', linestyle='-', color='r', label='Presión en la partícula central')

    # Add mean lines
    plt.axhline(y=mean_wall_pressure, color='b', linestyle='--', label='Promedio de presión en la pared')
    plt.axhline(y=mean_center_pressure, color='r', linestyle='--', label='Promedio de presión en la partícula central')

    # Set scientific notation for the x-axis with superscript
    ax = plt.gca()
    ax.xaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='x', scilimits=(0, 0))

    # Y-axis formatting
    ax.yaxis.set_major_formatter(ScalarFormatter(useMathText=True))
    ax.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

    print(f"Pressure in wall: min={min(pressures_in_wall)}, max={max(pressures_in_wall)}")
    print(f"Pressure in center particle: min={min(pressures_in_center_particle)}, max={max(pressures_in_center_particle)}")

    # Add labels and title
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Presión (N/m)')

    plt.grid(True)
    plt.legend()

    # Ensure the Y-axis starts from 0
    plt.ylim(bottom=0)

    # Show the plot
    plt.show()
    plt.savefig(f"pressure_over_time_v0_{v0}.png")


def calculate_pressure_in_center_particle(simulation_snapshots: List[SimulationSnapshot], center_particle_radius: float, particle_mass: float, time_interval: float) -> Dict[float, PressureDataInInterval]:
    # The key of the dict is the end of the time interval
    pressure_data_by_interval: Dict[float, PressureDataInInterval] = {}
    for simulation in simulation_snapshots:
        # Generate the corresponding dict key
        time_interval_end = simulation.collision_event.time // time_interval * time_interval + time_interval

        # Get or create interval info
        pressure_data_in_interval = pressure_data_by_interval.get(time_interval_end, PressureDataInInterval(interval_start=time_interval_end - time_interval,
                                                                                                            interval_end=time_interval_end))
        pressure_data_by_interval[time_interval_end] = pressure_data_in_interval


        # We are only interested in collisions with center particle
        if simulation.collision_event.collision_type == "wall":  # Discard wall collisions
            continue
        if simulation.collision_event.particle1.id != 0 and simulation.collision_event.particle2.id != 0:  # Discard collisions with other particles
            continue

        # The particle that is not the center particle
        particle = simulation.collision_event.particle1 if simulation.collision_event.particle1.id != 0 else simulation.collision_event.particle2

        # Calculate the normal velocity to the wall and get the particle mass
        vn = calculate_normal_velocity_to_center_particle(particle)

        # Update interval info
        pressure_data_in_interval.momentum_sum += 2 * particle_mass * vn
        pressure_data_in_interval.total_collisions += 1
        pressure_data_in_interval.pressure = pressure_data_in_interval.momentum_sum / (2 * pi * center_particle_radius * time_interval)
        pressure_data_by_interval[time_interval_end] = pressure_data_in_interval

    return pressure_data_by_interval


def calculate_pressure_in_wall(simulation_snapshots: List[SimulationSnapshot], circle_radius: float, particle_mass: float, time_interval: float) -> Dict[float, PressureDataInInterval]:
    # The key of the dict is the end of the time interval
    pressure_data_by_interval: Dict[float, PressureDataInInterval] = {}
    for simulation in simulation_snapshots:
        # Generate the corresponding dict key
        time_interval_end = simulation.collision_event.time // time_interval * time_interval + time_interval

        # Get or create interval info
        pressure_data_in_interval = pressure_data_by_interval.get(time_interval_end, PressureDataInInterval(interval_start=time_interval_end - time_interval,
                                                                                                            interval_end=time_interval_end))
        pressure_data_by_interval[time_interval_end] = pressure_data_in_interval

        # We are only interested in wall collisions
        if simulation.collision_event.collision_type != "wall":
            continue

        # Calculate the normal velocity to the wall and get the particle mass
        vn = calculate_normal_velocity_to_wall(simulation.collision_event.particle1)

        # Update interval info
        pressure_data_in_interval.momentum_sum += 2 * particle_mass * vn
        pressure_data_in_interval.total_collisions += 1
        pressure_data_in_interval.pressure = pressure_data_in_interval.momentum_sum / (2 * pi * circle_radius * time_interval)
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

    return abs(vn)


def calculate_normal_velocity_to_center_particle(particle: Particle) -> float:
    """Calculate the normal velocity of a particle to the center particle"""
    return calculate_normal_velocity_to_wall(particle)
