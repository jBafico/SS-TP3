package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;


@Getter
@AllArgsConstructor
public class Coordinates {
    private double x;
    private double y;

    public static Coordinates generateRandomCoordinatesInCircle(double wallRadius, double particleRadius){
        // generate random distance in the range [0, wallRadius - particleRadius]
        double distanceFromCenter = Math.random() * (wallRadius - particleRadius);
        // generate random angle in radians (from 0 to 2pi)
        double angle = Math.random() * 2 * Math.PI;

        // decompose the distance into x and y coordinates
        double x = distanceFromCenter * Math.cos(angle);
        double y = distanceFromCenter * Math.sin(angle);
        return new Coordinates(x, y);
    }
}