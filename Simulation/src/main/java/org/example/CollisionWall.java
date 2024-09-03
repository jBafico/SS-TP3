package org.example;

import java.util.Optional;

//Represent collision between a particle and a wall
public class CollisionWall extends CollisionEventAbstract<MovingParticle, Wall>{
    public CollisionWall(MovingParticle movingParticle, Wall wall, double time) {
        super(movingParticle, wall, time);
    }

    public Optional<CollisionEventAbstract<MovingParticle, Wall>> calculateCollision(MovingParticle movingParticle, Wall wall, double planeLength) {
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

}
