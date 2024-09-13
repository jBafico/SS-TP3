from dataclasses import dataclass
from typing import List


@dataclass
class Particle:
    id: int
    x: float
    y: float
    vx: float
    vy: float
    mass: float


@dataclass
class CollisionEvent:
    collision_type: str
    time: float


@dataclass
class GlobalParams:
    number_of_particles: int
    wall_radius: float
    particle_radius: float
    obstacle_radius: float
    velocity_modulus: float
    particle_mass: float
    max_events: int


@dataclass
class SimulationSnapshot:
    particles: List[Particle]
    collision_event: CollisionEvent


@dataclass
class SimulationOutput:
    global_params: GlobalParams
    simulations: List[SimulationSnapshot]
