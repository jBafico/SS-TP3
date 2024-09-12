package org.example;


import lombok.Getter;
import lombok.Setter;

import java.util.Optional;

@Getter
@Setter
public class Params {

    private int numberOfParticles;
    private double wallRadius;
    private double particleRadius;
    private double obstacleRadius;
    private double velocityModulus;
    private double particleMass;
    private Double obstacleMass;
    private int maxEvents;
}
