package org.example;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
public class CollisionEvent implements Comparable<CollisionEvent> {
    private double time;

    public int compareTo(CollisionEvent o) {
        return Double.compare(time, o.time);
    }
}
