package org.example;

import java.util.Optional;

public class Main {
    public static void main(String[] args) {
        System.out.println("Starting simulation!");

        // todo replace with json parameters
        int numberOfParticles = 10;
        double wallRadius = 100;
        double particleRadius = 1;
        double obstacleRadius = 3;
        double velocityModulus = 1;
        double particleMass = 1;
        Optional<Double> obstacleMass = Optional.empty();

        MDSimulation simulation = new MDSimulation(numberOfParticles, wallRadius, particleRadius, obstacleRadius, velocityModulus, particleMass, obstacleMass);
    }
}