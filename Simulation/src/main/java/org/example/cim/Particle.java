package com.example.myapp;

import lombok.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;


@Getter
@Setter
@ToString
@EqualsAndHashCode
@NoArgsConstructor
public class Particle {

    private int id;
    private double XCoordinate;
    private double YCoordinate;
    private double radius;
    private ArrayList<Integer> nearbyParticles;

    public Particle(int id,double XCoordinate, double YCoordinate, double radius) {
        this.id = id;
        this.XCoordinate = XCoordinate;
        this.YCoordinate = YCoordinate;
        this.radius = radius;
        nearbyParticles = new ArrayList<>();
    }

    public static List<Particle> generateRandomParticles(double L, int N, double r){
        List<Particle> particlesList = new ArrayList<>();
        Random random = new Random();
        double min = 0;
        double max = L;
        for (int i = 0; i < N ; i++){
            double x = min + (max - min) * random.nextDouble();
            double y = min + (max - min) * random.nextDouble();
            particlesList.add(new Particle(i,x,y,r));
        }

        return particlesList;
    }

    public boolean checkNeighbour(Particle p, double r, double L, boolean boundaryConditions){
        double distanceX, distanceY, directDistanceX, directDistanceY;
        //calculamos la distancia entre sus centros
        //primero la distancia en x
        directDistanceX = Math.abs(p.getXCoordinate() - XCoordinate);
        //si multiplicando por 2 se pasa de L podemos considerar que estan a una distancia mayor que L/2 por lo que estan en opuestos diferentes
        if(directDistanceX*2>L && !boundaryConditions) {
            distanceX = L - directDistanceX;
        }
        else {
            distanceX = directDistanceX;
        }

        //Ahora con Y
        directDistanceY = Math.abs(p.getYCoordinate() - YCoordinate);
        if(directDistanceY*2>L && !boundaryConditions) {
            distanceY = L - directDistanceY;
        }else {
            distanceY = directDistanceY;
        }

        double distance= Math.sqrt(Math.pow(distanceX, 2) + Math.pow(distanceY, 2));
        //Ahora restamos los radios de las particulas
        distance-=(radius + p.getRadius());

        return distance <= r;
    }

    public void addNeighbour(Particle p){
        if(!nearbyParticles.contains(p.getId())){
            nearbyParticles.add(p.getId());
        }
    }

}

