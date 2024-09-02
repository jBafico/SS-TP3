package com.example.myapp;

import lombok.Getter;
import lombok.Setter;

import java.util.ArrayList;



@Getter
@Setter
public class Cell {
    private final int cellNumber;
    private ArrayList<Particle> particles = new ArrayList<>();

    public Cell(int cellNumber) {
        this.cellNumber = cellNumber;
    }


    public void addParticle(Particle p) {
        particles.add(p);
    }

    @Override
    public String toString() {
        return "Cell{" +
                "cellNumber=" + cellNumber +
                ", particles=" + particles +
                '}';
    }

    public ArrayList<Integer> getCellIndexesToCheck(int M, boolean boundaryConditions){
        ArrayList<Integer> cellIndexes = new ArrayList<>();

        boolean hasCellUpside = false;
        boolean hasCellToTheRight = false;
        boolean hasCellDownside = false;
        cellIndexes.add(cellNumber);

        //revisar Celda superior
        if (boundaryConditions && cellNumber >= M) {
            cellIndexes.add(cellNumber - M);
            hasCellUpside = true;
        } else if (!boundaryConditions) {
            cellIndexes.add((cellNumber + (M*M) -M)%(M*M));
        }

        //Revisar celda de la derecha
        if (boundaryConditions && (cellNumber % M) != (M-1)) {
            cellIndexes.add(cellNumber + 1);
            hasCellToTheRight = true;
        }else if (!boundaryConditions) {
            if((cellNumber % M) != (M-1)){
                cellIndexes.add(cellNumber + 1);
            }
            else {
                cellIndexes.add(cellNumber - M + 1);
            }
        }

        //celda diagonal arriba derecha
        if (boundaryConditions && hasCellToTheRight && hasCellUpside) {
            cellIndexes.add(cellNumber - M + 1);
        }else if (!boundaryConditions) {
            if (cellNumber < (M - 1)) {
                cellIndexes.add(cellNumber + (M * M) - M + 1);
            } else {
                cellIndexes.add((cellNumber + (M * (M - 1)) - (M - 1)) % (M * M));
            }
        }

        if(boundaryConditions && cellNumber < ((M*M) - M - 1)){
            hasCellDownside = true;
        }

        //celda diagonal abajo derecha
        if (boundaryConditions && hasCellDownside && hasCellToTheRight) {
            cellIndexes.add(cellNumber + M + 1);
        }else if (!boundaryConditions) {
            if(cellNumber == (M*M)-1){
                cellIndexes.add(0);
            } else if (cellNumber%M == (M-1)) {
                cellIndexes.add(cellNumber + 1);
            } else if (cellNumber >= (M*(M-1))) {
                cellIndexes.add(cellNumber- (M*(M-1))+1);
            } else{
                cellIndexes.add((cellNumber+ M + 1)%(M*M));
            }

        }
        return cellIndexes;

    }
}
