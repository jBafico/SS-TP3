package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import javax.management.relation.RoleStatus;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.PriorityQueue;

public class MDSimulation {
    private final PriorityQueue<CollisionEvent> collisionEvents = new PriorityQueue<>();
    private List<Particle> particleList;
    private Wall wall;
    private int maxEvents;

    public MDSimulation(int n, double wallRadius, double particleRadius, double obstacleRadius, double v0, double particleMass, Optional<Double> obstacleMass, int maxEvents) {
        particleList = generateRandomMovingParticles(n, wallRadius, particleRadius, v0, particleMass, obstacleRadius, obstacleMass);
        wall = new Wall(wallRadius);
        this.maxEvents = maxEvents;
    }

    public void start (FileWriter writer){
        int events = 0;
        while (events < maxEvents){
            events++;

            // Update collision events
            updateCollisionEvents();
        }
    }

    private void updateCollisionEvents(){
        for (Particle p : particleList){
            // Check if particle collides with wall and add it
            Optional<WallCollisionEvent> wallCollisionEvent = p.collidesWithWall(wall);
            wallCollisionEvent.ifPresent(collisionEvents::add);

            // Check if particle collides with other particles and add it
            for (Particle q : particleList){
                // If the particles are the same, skip
                if (p.getId() == q.getId()){
                    continue;
                }

                // Check if two particles collide
                Optional<ParticleCollisionEvent> particleCollisionEvent = p.collidesWithParticle(q);

                // If there is no collision, skip
                if (particleCollisionEvent.isEmpty()) {
                    continue;
                }

                // If the collision event is already in the list, skip
                if (collisionEvents.contains(particleCollisionEvent.get())){
                    continue;
                }

                // Add the collision event to the list
                collisionEvents.add(particleCollisionEvent.get());
            }
        }
    }

    private List<Particle> generateRandomMovingParticles(int n, double wallRadius, double particleRadius, double v0, double particleMass, double obstacleRadius, Optional<Double> obstacleMass){
        List<Particle> generatedParticles = new ArrayList<>();

        // Generate middle obstacle
        Particle middleObstacle;
        if (obstacleMass.isPresent()){ // If it has mass, it is a MovingParticle
            middleObstacle = new MovingParticle(0, 0, 0, obstacleRadius, 0, 0, obstacleMass.get());
        } else { // If it does not have mass, it is a StaticParticle
            middleObstacle = new StaticParticle(0, 0, 0, obstacleRadius);
        }
        generatedParticles.add(middleObstacle);

        // Generate n moving particles
        while (generatedParticles.size() <= n){
            // Generate new particle with random coordinates and velocity direction
            Coordinates coordinates = Coordinates.generateRandomCoordinatesInCircle(wallRadius, particleRadius);
            Velocity velocity = Velocity.generateRandomVelocityOfModulus(v0);
            MovingParticle newParticle = new MovingParticle(generatedParticles.size(), coordinates.getX(), coordinates.getY(), particleRadius, velocity.getVx(), velocity.getVy(), particleMass);

            // Check if new particle collides with any other particle in the list
            boolean collides = false;
            for (Particle p : generatedParticles){ //TODO fix this logic
                if (newParticle.isCollidingWithParticle(p)){
                    continue;
                }
            }

            // If the new particle does not collide with any other particle, add it to the list
            if (!collides){
                generatedParticles.add(newParticle);
            }
        }
        return generatedParticles;
    }

}
