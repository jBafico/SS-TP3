package org.example;

import lombok.Getter;

@Getter
public class ParticleCollisionEvent extends CollisionEvent{
    private final Particle particle1;
    private final Particle particle2;

    public ParticleCollisionEvent(double time, Particle particle1, Particle particle2) {
        super(time);
        this.particle1 = particle1;
        this.particle2 = particle2;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof ParticleCollisionEvent that)) return false;
        return getTime() == that.getTime() && particle1.equals(that.particle1) && particle2.equals(that.particle2);
    }

    @Override
    public int hashCode() {
        int result = Double.hashCode(getTime());  // Hash code of the time field
        result = 31 * result + particle1.hashCode();  // Combine with hash of particle1
        result = 31 * result + particle2.hashCode();  // Combine with hash of particle2
    return result;
}
}
