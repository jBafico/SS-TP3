from classes import *  # Assuming this imports Particle, SimulationOutput, etc.
from typing import List

def parse_json_simulation(json_file) -> List[SimulationOutput]:
    return [
        SimulationOutput(
            global_params=GlobalParams(
                number_of_particles=current_simulation['global_params']['numberOfParticles'],
                wall_radius=current_simulation['global_params']['wallRadius'],
                particle_radius=current_simulation['global_params']['particleRadius'],
                obstacle_radius=current_simulation['global_params']['obstacleRadius'],
                velocity_modulus=current_simulation['global_params']['velocityModulus'],
                particle_mass=current_simulation['global_params']['particleMass'],
                max_events=current_simulation['global_params']['maxEvents']
            ),
            simulations={
                f"simulation_{i + 1}": [
                    SimulationSnapshot(
                        particles=[
                            Particle(
                                id=particle['id'],
                                x=particle['x'],
                                y=particle['y'],
                                vx=particle['vx'],
                                vy=particle['vy'],
                                mass=particle['mass'] if str(particle['mass']) != 'Infinity' else 1e100
                            ) for particle in snapshot['particles']
                        ],
                        collision_event=CollisionEvent(
                            collision_type=snapshot['collisionEvent']['collisionType'],
                            time=snapshot['collisionEvent']['time'],
                            particle1=(
                                Particle(
                                    id=snapshot['collisionEvent']['movingParticle']['id'],
                                    x=snapshot['collisionEvent']['movingParticle']['x'],
                                    y=snapshot['collisionEvent']['movingParticle']['y'],
                                    vx=snapshot['collisionEvent']['movingParticle']['vx'],
                                    vy=snapshot['collisionEvent']['movingParticle']['vy'],
                                    mass=snapshot['collisionEvent']['movingParticle']['mass'] if str(snapshot['collisionEvent']['movingParticle']['mass']) != 'Infinity' else 1e100
                                )
                            ) if snapshot['collisionEvent']['collisionType'] == 'wall' else (
                                Particle(
                                    id=snapshot['collisionEvent']['particle1']['id'],
                                    x=snapshot['collisionEvent']['particle1']['x'],
                                    y=snapshot['collisionEvent']['particle1']['y'],
                                    vx=snapshot['collisionEvent']['particle1']['vx'],
                                    vy=snapshot['collisionEvent']['particle1']['vy'],
                                    mass=snapshot['collisionEvent']['particle1']['mass'] if str(snapshot['collisionEvent']['particle1']['mass']) != 'Infinity' else 1e100
                                )
                            ),
                            particle2=(
                                Particle(
                                    id=snapshot['collisionEvent']['particle2']['id'],
                                    x=snapshot['collisionEvent']['particle2']['x'],
                                    y=snapshot['collisionEvent']['particle2']['y'],
                                    vx=snapshot['collisionEvent']['particle2']['vx'],
                                    vy=snapshot['collisionEvent']['particle2']['vy'],
                                    mass=snapshot['collisionEvent']['particle2']['mass'] if str(snapshot['collisionEvent']['particle2']['mass']) != 'Infinity' else 1e100
                                )
                            ) if 'particle2' in snapshot['collisionEvent'] else None
                        )
                    ) for snapshot in current_simulation['simulations'][i][f'simulation_{i + 1}']
                ] for i in range(len(current_simulation["simulations"]))
            }
        ) for current_simulation in json_file
    ]
