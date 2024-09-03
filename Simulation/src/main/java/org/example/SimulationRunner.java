package org.example;

import org.example.cim.Particle;

import java.util.List;

public class SimulationRunner {

    private final Particle centralParticle;
    private List<Particle> particleList;


    public SimulationRunner(int amountOfParticles, double L) {
        this.centralParticle = new Particle(amountOfParticles,L / 2, L / 2, 0.005);
        Particle.generateRandomParticles(L,amountOfParticles,0.001);
    }
}
