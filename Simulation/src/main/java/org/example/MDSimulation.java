package org.example;

import java.io.FileWriter;
import java.util.List;
import java.util.PriorityQueue;

public class MDSimulation {
    private PriorityQueue<CollisionEvent> collisionEvents= new PriorityQueue<>();
    private List<MovingParticle> particleList;
    private Wall wall;

    public MDSimulation(int n, double wallRadius, double particleRadius, double obstacleRadius, double v0, double particleMass, double obstacleMass) {
        //TODO inicializar todo

    }
    public void start(FileWriter writer){

    }

    private List<MovingParticle> generateRandomMovingParticles(int n, double wallRadius, double particleRadius, double v0, double particleMass){

    }


}
