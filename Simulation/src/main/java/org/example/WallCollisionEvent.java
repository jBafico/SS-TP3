package org.example;

import lombok.Getter;

@Getter
public class WallCollisionEvent extends CollisionEvent {
    private final MovingParticle movingParticle;

    public WallCollisionEvent(double time, MovingParticle movingParticle) {
        super(time);
        this.movingParticle = movingParticle;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof WallCollisionEvent that)) return false;
        return getTime() == that.getTime() && movingParticle.equals(that.movingParticle);
    }

    @Override
    public int hashCode() {
        int result = Double.hashCode(getTime());  // Hash code of the time field
        result = 31 * result + movingParticle.hashCode();  // Combine with hash of movingParticle
        return result;
    }
}
