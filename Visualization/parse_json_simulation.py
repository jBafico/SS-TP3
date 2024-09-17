from classes import *


def parse_json_simulation(json_file) -> SimulationOutput:
    def parse_collision_event(collision_event_data):
        collision_type = collision_event_data['collisionType']
        time = collision_event_data['time']

        if collision_type == 'wall':
            # For a wall collision, we only have one particle (movingParticle), so particle2 is None
            particle1_data = collision_event_data['movingParticle']
            particle1 = Particle(
                id=particle1_data['id'],
                x=particle1_data['x'],
                y=particle1_data['y'],
                vx=particle1_data['vx'],
                vy=particle1_data['vy'],
                mass=particle1_data['mass']
            )
            return CollisionEvent(
                collision_type=collision_type,
                time=time,
                particle1=particle1,
                particle2=None
            )

        elif collision_type == 'particles':
            # For a particle collision, we have two particles: particle1 and particle2
            particle1_data = collision_event_data['particle1']
            particle2_data = collision_event_data['particle2']
            particle1 = Particle(
                id=particle1_data['id'],
                x=particle1_data['x'],
                y=particle1_data['y'],
                vx=particle1_data['vx'],
                vy=particle1_data['vy'],
                mass=particle1_data['mass']
            )
            particle2 = Particle(
                id=particle2_data['id'],
                x=particle2_data['x'],
                y=particle2_data['y'],
                vx=particle2_data['vx'],
                vy=particle2_data['vy'],
                mass=particle2_data['mass']
            )
            return CollisionEvent(
                collision_type=collision_type,
                time=time,
                particle1=particle1,
                particle2=particle2
            )

        else:
            raise ValueError(f"Unknown collision type: {collision_type}")

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
                collision_event=parse_collision_event(snapshot['collisionEvent'])
            ) for snapshot in json_file['simulations']
        ]
    )
