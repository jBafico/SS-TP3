package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public abstract class CollisionEvent implements Comparable<CollisionEvent> {
    private double time;

    @Override
    public int compareTo(CollisionEvent o) {
        return Double.compare(time, o.time);
    }

    @Override
    public abstract boolean equals(Object o);

    @Override
    public abstract int hashCode();
}
