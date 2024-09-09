package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.util.Optional;

@AllArgsConstructor
@Getter
@Setter
public abstract class Particle {
    private int id;
    private double x;
    private double y;
    private double r;
    private double vx;
    private double vy;
    private double mass;

    // Returns the event of collision with another particle if present
    public Optional<ParticleCollisionEvent> collidesWithParticle(Particle p){
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

    public boolean isCollidingWithParticle(Particle p){
        final double deltaX = x - p.getX();
        final double deltaY = y - p.getY();
        final double sigma = r + p.getR();
        final double deltaPosition= Math.sqrt(Math.pow(deltaX, 2) + Math.pow(deltaY, 2));

        return (deltaPosition-sigma<0);
    }

    // Returns the event of collision with the wall if present
    public abstract Optional<WallCollisionEvent> collidesWithWall(Wall wall);


    // Advances paticle to timestep
    public abstract void update(double timestep);

    // Modifies vx and vy for this particle
    public abstract void bounce(Particle p);

    // Modifies vx and vy for this particle
    public abstract void bounceWithWall(Wall wall);


    //We only want to say that two particles are equal if they have the same id
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Particle that)) return false;
        return id == that.getId();
    }
}
