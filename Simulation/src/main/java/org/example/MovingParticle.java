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
        if(getMass()!=Double.POSITIVE_INFINITY) {
            //we are going to use the cuadratic formula to calculate the collision time
            // Vx^2 + Vy^2
            final double a= Math.pow(getVx(), 2) + Math.pow(getVy(), 2);

            // (2*x*Vx)+(2*y*Vy)
            final double b= (2*getX()*getVx())+(2*getY()*getVy());

            // x^2+y^2+(R-r)^2
            final double c=Math.pow(getX(), 2) + Math.pow(getY(), 2) - Math.pow(wall.getRadius()- getR(), 2);

            // Cuadratic formula
            final double det=Math.sqrt(Math.pow(b,2) - 4*a*c);
            final double t1= (((-1)*b)+det)/(2*a);
            return Optional.of(new WallCollisionEvent(t1, this));
        }
        return Optional.empty();
    }

    @Override
    public void update(double timestep) { //You have to pass the DeltaTimestep between events
        if(getMass()!=Double.POSITIVE_INFINITY){
            setX(getX() + (getVx()*timestep));
            setY(getY() + (getVy()*timestep));
        }
    }

    @Override
    public void bounce(Particle p) {
        final double deltaX=p.getX()- getX();
        final double deltaY=p.getY()- getY();
        final double deltaVx=p.getVx()- getVx();
        final double deltaVy=p.getVy()- getVy();
        final double sigma= p.getR()+ getR();

        //Papers formulas on Page 3
        double j;
        if(p.getMass()!=Double.POSITIVE_INFINITY){
            j = 2 * getMass() * p.getMass() * (deltaVx * deltaX + deltaVy * deltaY) / (sigma * (getMass() + p.getMass()));
        }
        else {
            j= (2 * getMass() * (deltaVx* deltaX + deltaVy * deltaY))/(sigma * ((getMass()/p.getMass()) + 1));
        }
        final double jx = j * deltaX / sigma;
        final double jy = j * deltaY / sigma;

        this.setVx(getVx() + jx / getMass());
        this.setVy(getVy() + jy / getMass());
        if(p.getMass()!=Double.POSITIVE_INFINITY){
            p.setVx(p.getX() - jx / p.getMass());
            p.setVy(p.getY() - jy / p.getMass());
        }
    }

    @Override
    public void bounceWithWall(Wall wall) { // The particle is already at the collision point
        //First we calculate the distance from the center (0,0)
        final double distance= Math.sqrt(Math.pow(getX(),2) + Math.pow(getY(),2));

        //We calculate the collision normal
        final double nx= getX()/distance;
        final double ny= getY()/distance;

        //We calculate the dot product
        final double dotProduct= getVx()*nx+getVy()*ny;

        //Update the velocity
        setVx(getVx()-(2*dotProduct*nx));
        setVy(getVy()-(2*dotProduct*ny));
    }
}
