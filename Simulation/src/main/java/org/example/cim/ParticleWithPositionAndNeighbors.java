package com.example.myapp;

import java.util.List;

public record ParticleWithPositionAndNeighbors(int id , double x, double y, List<Integer> neighbors) {
}
