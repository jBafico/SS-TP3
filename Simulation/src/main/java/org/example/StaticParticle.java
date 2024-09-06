package org.example;

import java.util.Optional;

public class StaticParticle extends Particle {
    public StaticParticle(int id, double x, double y, double r) {
        super(id, x, y, r, 0, 0, Double.POSITIVE_INFINITY);
    }

    @Override
    public Optional<WallCollisionEvent> collidesWithWall(Wall wall) {
        // It never collides with a wall because it is static
        return Optional.empty();
    }

    @Override
    public void update(double timestep) {
        // It does not move because it is static
    }

    @Override
    public void bounce(Particle p) {
        // It does not move because it is static
    }

    @Override
    public void bounceWithWall(Wall wall) {
        // It does not move because it is static
    }
}
