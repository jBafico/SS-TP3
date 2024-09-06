package org.example;


import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

import java.util.Optional;

@Getter
@Setter
@ToString
@AllArgsConstructor
public class MovingParticle {
    private int id;
    private double x;
    private double y;
    private double r;
    private double vx;
    private double vy;
    private double mass;

    public Optional<ParticleCollisionEvent> collidesWithParticle(MovingParticle p){
        final double deltaX = x - p.getX();
        final double deltaY = y - p.getY();
        final double deltaVx = vx - p.getVx();
        final double deltaVy = vy - p.getVy();

        //Formulas of Class 3 slide 14
        final double sigma = r + p.getR();
        final double d = Math.pow(deltaVx * deltaX + deltaVy * deltaY, 2) - (deltaVx * deltaVx + deltaVy * deltaVy) * (deltaX * deltaX + deltaY * deltaY - sigma * sigma);

        if (deltaVx * deltaX + deltaVy * deltaY >= 0 || d < 0) {
            return Optional.empty();
        }

        final double time = -1 * (deltaVx * deltaX + deltaVy * deltaY + Math.sqrt(d)) / (deltaVx * deltaVx + deltaVy * deltaVy);
        return Optional.of(new ParticleCollisionEvent(time, this, p));
    }

    public Optional<WallCollisionEvent> collidesWithWall(Wall wall){
        //TODO implement
        return Optional.empty();
    }

    //Advances paticle to timestep
    public void update(double timestep){

    }

    //Modifies vx and vy for this particle and the particle that is colliding with
    public void bounce(MovingParticle p){

    }

    //Modifies vx and vy for this particle
    public void bounceWithWall(Wall wall){

    }


}
