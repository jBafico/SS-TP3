import matplotlib.pyplot as plt
import imageio
import io
from load_most_recent_json import load_most_recent_simulation_json

# Function to assign color to particles based on collision events
def assign_color_to_particle(id, collision_event):
    if collision_event["collisionType"] == "particles" and (id == collision_event["particle1"]["id"] or id == collision_event["particle2"]["id"]):
        return "purple"
    if collision_event["collisionType"] == "wall" and id == collision_event["movingParticle"]["id"]:
        return "purple"
    if id == 0:
        return "green"
    return "red"

# Function to plot a single simulation frame and return as an in-memory image
def plot_simulation_frame_in_memory(particles, circle_radius, frame_num, collision_event):
    fig, ax = plt.subplots()

    # Draw the circular boundary (the box)
    circle = plt.Circle((0, 0), circle_radius, color='blue', fill=False, linewidth=2)
    ax.add_artist(circle)

    # Plot particles as non-filled red circles
    for particle in particles:
        x, y, r, id = particle['x'], particle['y'], particle['r'], particle['id']
        color_to_particle = assign_color_to_particle(id, collision_event)
        particle_circle = plt.Circle((x, y), r, color=color_to_particle, fill=False, linewidth=2)
        ax.add_artist(particle_circle)

    # Set limits and aspect ratio
    ax.set_xlim(-circle_radius, circle_radius)
    ax.set_ylim(-circle_radius, circle_radius)
    ax.set_aspect('equal', 'box')

    # Add labels and title
    ax.set_xlabel('X position')
    ax.set_ylabel('Y position')
    plt.title(f'Simulation Frame {frame_num}')

    # Save the frame as an in-memory image (BytesIO)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)  # Rewind the buffer

    return buf

# Function to create a GIF from simulation frames in memory
def create_simulation_gif_in_memory(data):
    # Read the simulation data from the JSON file
    circle_radius = data["global_params"]["wallRadius"]
    simulations = data['simulations']

    # List to store in-memory images
    frames = []

    # Generate a frame for each simulation
    for i, simulation in enumerate(simulations):
        particles = simulation['particles']
        collision_event = simulation['collisionEvent']
        frame_buf = plot_simulation_frame_in_memory(particles, circle_radius, i, collision_event)
        frames.append(imageio.imread(frame_buf))  # Read the in-memory image into a format imageio can handle

    # Create a GIF directly from in-memory images
    gif_buf = io.BytesIO()
    with imageio.get_writer(gif_buf, format='GIF', mode='I', duration=3) as writer:
        for frame in frames:
            writer.append_data(frame)

    gif_buf.seek(0)  # Rewind the buffer to read the GIF
    return gif_buf

# Example usage:
json_file = load_most_recent_simulation_json("./files")  # The path to your JSON file
circle_radius = json_file["global_params"]["wallRadius"]  # Radius of the circular box

# Generate the GIF in memory
gif_in_memory = create_simulation_gif_in_memory(json_file)

# Save or use the GIF as needed, for example, to save to a file:
with open("./Visualization/simulation_output.gif", "wb") as f:
    f.write(gif_in_memory.getvalue())
