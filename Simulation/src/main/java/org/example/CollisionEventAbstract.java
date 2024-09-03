package org.example;

import lombok.Getter;

import java.util.Optional;

//Class that represents a collision event between 2 particles or a particle and a wall
@Getter
public abstract class CollisionEventAbstract<TObject1, TObject2> {
    private final TObject1 object1;
    private final TObject2 object2;
    private double time;

    public CollisionEventAbstract(TObject1 object1, TObject2 object2, double time) {
        this.object1 = object1;
        this.object2 = object2;
        this.time = time;
    }

}
