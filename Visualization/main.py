from load_most_recent_json import load_most_recent_simulation_json
from parse_json_simulation import parse_json_simulation
from calculate_pressure import plot_pressure_over_time
from graph_kinetic_energy import plot_pressure_by_kinetic_energy_for_simulations


def main():
    # --------------- INITIAL CONFIGS ----------------------
    plot_pressure_evolution_over_time = True
    plot_pressure_by_kinetic_energy = True

    print("Parsing JSON data...")
    # Load the most recent simulation JSON data
    json_data = load_most_recent_simulation_json('../files')
    simulation_outputs = parse_json_simulation(json_data)
    print("Finished parsing JSON data.")

    if plot_pressure_evolution_over_time:
        print("Plotting pressure data...")
        [[plot_pressure_over_time(simulation_snapshot, simulation_output.global_params.wall_radius, simulation_output.global_params.obstacle_radius, simulation_output.global_params.particle_mass, simulation_output.global_params.velocity_modulus) for simulation_snapshot in simulation_output.simulations.values()] for simulation_output in simulation_outputs]
        print("Finished plotting pressure data.")

    if plot_pressure_by_kinetic_energy:
        print("Plotting kinetic energy...")
        plot_pressure_by_kinetic_energy_for_simulations(simulation_outputs)
        print("Finished plotting kinetic energy.")


if __name__ == '__main__':
    main()
