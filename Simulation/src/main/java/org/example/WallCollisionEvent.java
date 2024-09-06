package org.example;

import lombok.Getter;

@Getter
public class WallCollisionEvent extends CollisionEvent {
    private final MovingParticle movingParticle;


    public WallCollisionEvent(double time, MovingParticle movingParticle) {
        super(time);
        this.movingParticle = movingParticle;
    }
}
