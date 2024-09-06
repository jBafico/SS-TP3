package org.example;

import lombok.Getter;

@Getter
public class ParticleCollisionEvent extends CollisionEvent{
    private final Particle particle1;
    private final Particle particle2;

    public ParticleCollisionEvent(double time, Particle particle1, Particle particle2) {
        super(time);
        this.particle1 = particle1;
        this.particle2 = particle2;
    }
}
