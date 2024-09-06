package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;

@Getter
@AllArgsConstructor
public class Velocity {
    private double vx;
    private double vy;

    public static Velocity generateRandomVelocityOfModulus(double v0){
        // generate random angle in radians (from 0 to 2pi)
        double angle = Math.random() * 2 * Math.PI;

        // decompose the velocity into x and y components
        double vx = v0 * Math.cos(angle);
        double vy = v0 * Math.sin(angle);
        return new Velocity(vx, vy);
    }
}
