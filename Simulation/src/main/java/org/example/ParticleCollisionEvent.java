package org.example;

import lombok.Getter;

@Getter
public class ParticleCollisionEvent extends CollisionEvent{
    private final MovingParticle particle1;
    private final MovingParticle particle2;

    public ParticleCollisionEvent(double time, MovingParticle particle1, MovingParticle particle2) {
        super(time);
        this.particle1 = particle1;
        this.particle2 = particle2;
    }

}
