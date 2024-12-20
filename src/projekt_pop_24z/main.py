from src.projekt_pop_24z.swarm.models import Particle


def main():
    particle = Particle(dimensions=2)
    particle.initialize_particle(bounds=[[0, 1], [0, 1]])
    print(particle)
    return 0


if __name__ == "__main__":
    main()
