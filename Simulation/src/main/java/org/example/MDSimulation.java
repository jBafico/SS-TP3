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

    public MDSimulation(int n, double wallRadius, double particleRadius, double obstacleRadius, double v0, double particleMass, Optional<Double> obstacleMass) {
        particleList = generateRandomMovingParticles(n, wallRadius, particleRadius, v0, particleMass, obstacleRadius, obstacleMass);
        ;
    }
    public void start(FileWriter writer){

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
            for (Particle p : generatedParticles){
                if (newParticle.collidesWithParticle(p).isPresent()){
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
