from classes import *


def parse_json_simulation(json_file) -> SimulationOutput:
    return SimulationOutput(
        global_params=GlobalParams(
            number_of_particles=json_file['global_params']['numberOfParticles'],
            wall_radius=json_file['global_params']['wallRadius'],
            particle_radius=json_file['global_params']['particleRadius'],
            obstacle_radius=json_file['global_params']['obstacleRadius'],
            velocity_modulus=json_file['global_params']['velocityModulus'],
            particle_mass=json_file['global_params']['particleMass'],
            max_events=json_file['global_params']['maxEvents']
        ),
        simulations=[
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
                    time=snapshot['collisionEvent']['time']
                )
            ) for snapshot in json_file['simulations']
        ]
    )
