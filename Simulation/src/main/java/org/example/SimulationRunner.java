package org.example;

import org.example.cim.Particle;

import java.util.List;
import java.util.Optional;

public class SimulationRunner {

    private final Particle centralParticle;
    private List<MovingParticle> particleList;

    private final double planeLength;


    public SimulationRunner(int amountOfParticles, double L, double initialSpeed, double initialMass, SimulationHistory simulationHistory) {
        this.planeLength = L;
        this.centralParticle = new Particle(amountOfParticles,planeLength , planeLength, 0.005);
        this.particleList = Particle.generateRandomParticles(L,amountOfParticles,0.001,initialSpeed, initialMass, centralParticle);
    }


    public void runSimulation(){


        double lowestColisionTime = Double.MAX_VALUE;

        for (MovingParticle p : particleList){
            //Calculamos tiempo minimo para colisionar con la pared o con las particulas
            double lowestCollisionWithWall = lowestTimeTillWallCollision(p);
            double lowestCollisionWithParticle = lowestTimeTillParticleCollision(p, 1);
            if (lowestCollisionWithWall < lowestColisionTime){
                lowestColisionTime = lowestCollisionWithWall;
            }



        }

    }


    private double lowestTimeTillParticleCollision(MovingParticle currentParticle,int currentIteration){

        //TODO: llegue hasta aca
        double minTime = Double.MAX_VALUE;
        for (MovingParticle p : particleList){
            //si analizo la particula que estoy parado o no hubo un cambio desde la epoca anterior paso con la siguiente
            if (p.equals(currentParticle) || p.getLatestIterationChange() != currentIteration - 1){
                continue;
            }



        }
        return 0;

    }

    private double lowestTimeTillWallCollision(MovingParticle p){
        double minColisionTime = Double.MAX_VALUE;
        for (Wall wall : Wall.values()){
            Optional<CollisionWall> maybeWallColision = ColisionHelpers.calculateCollisionWithWall(p,wall,planeLength);
            if (maybeWallColision.isPresent()){
                CollisionWall collisionWall = maybeWallColision.get();
                if (collisionWall.getTime() < minColisionTime){
                    minColisionTime = collisionWall.getTime();
                }
            }
        }
        return minColisionTime;
    }

}
