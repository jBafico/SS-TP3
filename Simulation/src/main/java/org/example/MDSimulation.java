package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import javax.management.relation.RoleStatus;
import java.io.FileWriter;
import java.util.*;

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
        double simulationTime = 0;
        while (events < maxEvents){
            events++;
            // Update collision events
            updateCollisionEvents(simulationTime);

            //We get the first collision event
            if(!collisionEvents.isEmpty()){
                CollisionEvent collisionEvent= collisionEvents.poll();
                double eventTime=collisionEvent.getTime();

                //Update the position of all particles till the time of the event
                for (Particle p: particleList){
                    p.update(eventTime-simulationTime);
                }

                //Now that we already moved all the particles, we resolve the collision that modifies the velocity of the ones involved
                //If the collision is a WallCollisionEvent
                if(collisionEvent instanceof WallCollisionEvent){
                    Particle particle=((WallCollisionEvent) collisionEvent).getMovingParticle();
                    //we modify the velocity
                    particle.bounceWithWall(wall);

                    //Now we need to delete events that contain the particle
                    deleteCollisionEvents(particle);

                }else{//if the collision is a particleCollisionEvent
                    Particle particle1=((ParticleCollisionEvent) collisionEvent).getParticle1();
                    Particle particle2=((ParticleCollisionEvent) collisionEvent).getParticle2();
                    //we modify the velocity
                    particle1.bounce(particle2);

                    //Now we need to delete events that contain both particles
                    deleteCollisionEvents(particle1);
                    deleteCollisionEvents(particle2);
                }

                //lastly we update the simulation time
                simulationTime += eventTime;
            }
        }
    }

    //I added simulationTime so that the new events are calculated with the simulationTime included
    private void updateCollisionEvents(double simulationTime){
        for (Particle p : particleList){
            // Check if particle collides with wall and add it
            Optional<WallCollisionEvent> wallCollisionEvent = p.collidesWithWall(wall);
            if(wallCollisionEvent.isPresent()){
                //we add the current simulation time to the time till collision because the position of the particles have been updated
                CollisionEvent collisionEvent = wallCollisionEvent.get();
                collisionEvent.setTime(simulationTime+collisionEvent.getTime());
                if (!collisionEvents.contains(collisionEvent)){
                    collisionEvents.add(collisionEvent);
                }

            }



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
                particleCollisionEvent.get().setTime(simulationTime+particleCollisionEvent.get().getTime());

                // If the collision event is already in the list, skip
                if (collisionEvents.contains(particleCollisionEvent.get())){
                    continue;
                }

                // Add the collision event to the list
                collisionEvents.add(particleCollisionEvent.get());
            }
        }
    }

    //Method used to delete events of particle p from the collision event priority queue
    private void deleteCollisionEvents(Particle p){
        collisionEvents.removeIf(collisionEvent -> collisionEvent.involvesParticle(p));
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
                if (newParticle.isCollidingWithParticle(p)){
                    collides=true;
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
