package org.example;


import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.Optional;

@Getter
@Setter
@ToString
public class MovingParticle extends Particle {
    public MovingParticle(int id, double x, double y, double r, double vx, double vy, double mass) {
        super(id, x, y, r, vx, vy, mass);
    }

    @Override
    public Optional<WallCollisionEvent> collidesWithWall(Wall wall) {
        // todo
        return Optional.empty();
    }

    @Override
    public void update(double timestep) {
        // todo
    }

    @Override
    public void bounce(Particle p) {
        // todo
    }

    @Override
    public void bounceWithWall(Wall wall) {
        // todo
    }
}
