package org.example;


import lombok.Getter;
import lombok.Setter;
import lombok.ToString;
import org.example.cim.Particle;

import java.util.ArrayList;

@Getter
@Setter
@ToString
public class MovingParticle extends Particle {
    private double velocity;
    private double angle;
    private double mass;

    public MovingParticle(int id,double XCoordinate, double YCoordinate, double radius, double velocity, double angle, double mass) {
        super(id, XCoordinate, YCoordinate, radius);
        this.velocity = velocity;
        this.angle = angle;
        this.mass = mass;
    }
}
