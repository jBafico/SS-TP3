import matplotlib.pyplot as plt
import imageio
import os
from load_most_recent_json import load_most_recent_simulation_json

import matplotlib.pyplot as plt
import os


def assing_color_to_particle(id, collision_event):
    if collision_event["collisionType"] == "particles" and ( id == collision_event["particle1"]["id"] or id == collision_event["particle2"]["id"] ):
        return "purple"
    if collision_event["collisionType"] == "wall" and id == collision_event["movingParticle"]["id"]:
        return "purple"
    if id == 0:
        return "green"
    return "red"

# Function to plot a single simulation frame
def plot_simulation_frame(particles, circle_radius, frame_num, output_dir, collision_event):
    fig, ax = plt.subplots()

    # Draw the circular boundary (the box)
    circle = plt.Circle((0, 0), circle_radius, color='blue', fill=False, linewidth=2)
    ax.add_artist(circle)

    # Plot particles as non-filled red circles
    for particle in particles:
        x, y, r, id = particle['x'], particle['y'], particle['r'], particle['id']
        #particulas que interactuaron en != color
        color_to_particle = assing_color_to_particle(id,collision_event)
        particle_circle = plt.Circle((x, y), r, color=color_to_particle, fill=False, linewidth=2)
        ax.add_artist(particle_circle)

    # Set limits and aspect ratio
    ax.set_xlim(-circle_radius - 1, circle_radius + 1)
    ax.set_ylim(-circle_radius - 1, circle_radius + 1)
    ax.set_aspect('equal', 'box')

    # Add labels and title
    ax.set_xlabel('X position')
    ax.set_ylabel('Y position')
    plt.title(f'Simulation Frame {frame_num}')

    # Save the frame as a PNG file
    frame_path = os.path.join(output_dir, f"frame_{frame_num}.png")
    plt.savefig(frame_path)
    plt.close(fig)

    return frame_path


# Function to create a GIF from simulation frames
def create_simulation_gif(data):
    # Read the simulation data from the JSON file

    


    circle_radius = json_file["global_params"]["wallRadius"]  
    simulations = data['simulations']

    output_gif = './Visualization/simulations'  # The name of the output GIF file
    os.makedirs(output_gif, exist_ok=True)

    # Output directory for frames
    output_dir = "./Visualization/frames"
    os.makedirs(output_dir, exist_ok=True)

    # List to store paths of the frames
    frames = []

    # Generate a frame for each simulation
    for i, simulation in enumerate(simulations):
        particles = simulation['particles']
        collision_event = simulation['collisionEvent']
        frame_path = plot_simulation_frame(particles, circle_radius, i, output_dir,collision_event)
        frames.append(frame_path)

    # Create a GIF from the saved frames
    with imageio.get_writer(output_gif, mode='I', duration=3) as writer:
        for frame_path in frames:
            image = imageio.imread(frame_path)
            writer.append_data(image)

    # Optionally, clean up the frame files after creating the GIF
    # for frame_path in frames:
    #     os.remove(frame_path)

# Example usage:
json_file = load_most_recent_simulation_json("./files")  # The path to your JSON file
circle_radius = json_file["global_params"]["wallRadius"]              # Radius of the circular box

create_simulation_gif(json_file)
