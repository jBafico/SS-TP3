package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.util.List;


@Getter
@Setter
@AllArgsConstructor
public class SimulationSnapshot {
    List<Particle> particles;
    CollisionEvent collisionEvent;
}
