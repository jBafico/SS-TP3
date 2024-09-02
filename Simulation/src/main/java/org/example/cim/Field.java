package com.example.myapp;

import lombok.Getter;
import lombok.Setter;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


@Getter
@Setter
public class Field {
    private final float L;
    private final int M;
    private final int N; //numero de particulas
    private Cell[] cells;

    public Field(float l, int m, int n) {
        L = l;
        M = m;
        N = n;
        cells = new Cell[m * m];
        for (int i = 0; i < m*m; i++) {
            Cell cell= new Cell(i);
            cells[i] = cell;
        }
    }


    public void setParticlesInField(List<Particle> particles) {
        for (var particle : particles){
            //get cell index for particle
            int xIndex = (int) Math.floor(particle.getXCoordinate() / ((double) L / (double) M));
            int yIndex = (int) Math.floor(particle.getYCoordinate() / ((double) L / (double) M));
            int finalIndex =  xIndex + (yIndex * M);
            cells[finalIndex].addParticle(particle);
        }

    }

    //r es el radio de neighbour
    public void CIM(double r, boolean boundaryConditions){
        for (Cell cell : cells){
            ArrayList<Integer> cellsToCheck = cell.getCellIndexesToCheck(M, boundaryConditions);
            for (Particle particle : cell.getParticles()){
                for(int cellIndex : cellsToCheck){
                    for (Particle particleToCompare : cells[cellIndex].getParticles()){
                        if (!particle.equals(particleToCompare) && particle.checkNeighbour(particleToCompare, r, L, boundaryConditions)){
                            particle.addNeighbour(particleToCompare);
                            particleToCompare.addNeighbour(particle);
                        }
                    }
                }
            }
        }
    }

    @Override
    public String toString() {
        return "Field{" +
                "cells=" + Arrays.toString(cells) +
                '}';
    }
}
