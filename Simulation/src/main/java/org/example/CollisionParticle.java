package org.example;

import java.util.Optional;

//represents collision between 2 particles
public class CollisionParticle extends CollisionEventAbstract<MovingParticle, MovingParticle>{

    public CollisionParticle(MovingParticle movingParticle1, MovingParticle movingParticle2, double time) {
        super(movingParticle1, movingParticle2, time);
    }

    public Optional<CollisionEventAbstract<MovingParticle, MovingParticle>> calculateCollision(MovingParticle movingParticle1, MovingParticle movingParticle2, double planeLength) {
        //First we calculate the velocity of the particles on the X and Y axis
        final double vx1 = movingParticle1.getVelocity() * Math.cos(movingParticle1.getAngle());
        final double vy1 = movingParticle1.getVelocity() * Math.sin(movingParticle1.getAngle());
        final double vx2 = movingParticle2.getVelocity() * Math.cos(movingParticle2.getAngle());
        final double vy2 = movingParticle2.getVelocity() * Math.sin(movingParticle2.getAngle());

        //Then we calculate the distance between the particles and the difference in their velocities
        final double deltaX = movingParticle2.getXCoordinate() - movingParticle1.getXCoordinate();
        final double deltaY = movingParticle2.getYCoordinate() - movingParticle1.getYCoordinate();
        final double deltaVx = vx2 - vx1;
        final double deltaVy = vy2 - vy1;

        //Formulas of Class 3 slide 14
        final double sigma = movingParticle1.getRadius() + movingParticle2.getRadius();
        final double d = Math.pow(deltaVx * deltaX + deltaVy * deltaY, 2) - (deltaVx * deltaVx + deltaVy * deltaVy) * (deltaX * deltaX + deltaY * deltaY - sigma * sigma);

        if (deltaVx * deltaX + deltaVy * deltaY >= 0 || d < 0) {
            return Optional.empty();
        }

        final double time = -1 * (deltaVx * deltaX + deltaVy * deltaY + Math.sqrt(d)) / (deltaVx * deltaVx + deltaVy * deltaVy);
        return Optional.of(new CollisionParticle(movingParticle1, movingParticle2, time));
    }
}
