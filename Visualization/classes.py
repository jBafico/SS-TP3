from dataclasses import dataclass
from typing import List, Dict


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
    particle1 : Particle 
    particle2: Particle


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
    simulations: Dict[str,List[SimulationSnapshot]]
