package org.example;

import java.util.Optional;

//Esta clase tiene los helpers para calcular tiempos de colisiones
public class ColisionHelpers {

    private ColisionHelpers(){}

    public static Optional<CollisionWall> calculateCollisionWithWall(MovingParticle movingParticle, Wall wall, double planeLength){
        //First we calculate the velocity of the particle on the X and Y axis
        final double vx = movingParticle.getVelocity() * Math.cos(movingParticle.getAngle());
        final double vy = movingParticle.getVelocity() * Math.sin(movingParticle.getAngle());
        Double time = null;


        if (wall == Wall.LEFT && vx < 0) { //VelocityX has to be negative for the particle to be able to hit the left wall
            time = (0 + movingParticle.getRadius() - movingParticle.getXCoordinate()) / vx;
        } else if (wall == Wall.RIGHT && vx > 0) { //VelocityX has to be positive for the particle to be able to hit the right wall
            time = (planeLength - movingParticle.getRadius() - movingParticle.getXCoordinate()) / vx;
        } else if (wall == Wall.BOTTOM && vy < 0) { //VelocityY has to be negative for the particle to be able to hit the bottom wall
            time = (0 + movingParticle.getRadius() - movingParticle.getYCoordinate()) / vy;
        } else if (wall == Wall.TOP && vy > 0){ //VelocityY has to be positive for the particle to be able to hit the upper wall
            time = (planeLength - movingParticle.getRadius() - movingParticle.getYCoordinate()) / vy;
        }
        if (time == null) {
            return Optional.empty();
        }
        return Optional.of(new CollisionWall(movingParticle, wall, time));
    }


    public static Optional<CollisionParticle> calculateCollisionWithParticle(MovingParticle movingParticle1, MovingParticle movingParticle2, double planeLength){
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
