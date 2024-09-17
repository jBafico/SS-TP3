from classes import *


def parse_json_simulation(json_file) -> List[SimulationOutput]:


    return [ SimulationOutput(
        global_params=GlobalParams(
            number_of_particles=current_simulation['global_params']['numberOfParticles'],
            wall_radius=current_simulation['global_params']['wallRadius'],
            particle_radius=current_simulation['global_params']['particleRadius'],
            obstacle_radius=current_simulation['global_params']['obstacleRadius'],
            velocity_modulus=current_simulation['global_params']['velocityModulus'],
            particle_mass=current_simulation['global_params']['particleMass'],
            max_events=current_simulation['global_params']['maxEvents']
        ),
        simulations={ f"simulation_{i + 1}" : [
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
                    particle1 = snapshot['collisionEvent'].get("particle1",None),
                    particle2 = snapshot['collisionEvent'].get("particle2",None)
                )
            ) for snapshot in current_simulation['simulations'][i][f'simulation_{i + 1}']
        ] for i in range(len(current_simulation["simulations"]))}
    ) for current_simulation in json_file]
