import unittest

from perestroika.genetics import Neat


class TestGenetics(unittest.TestCase):
    def test_create_new_genome(self):
        neat = Neat(2, 2, 10)
        genome = neat.create_new_genome()
        self.assertEqual(genome.get_nodes_amount(), 4)
        self.assertEqual(genome.get_connections_amount(), 0)
        return

    def test_create_connections(self):
        neat = Neat(2, 2, 10)
        genome = neat.create_new_genome()
        neat.create_connection(genome, 0, 1)
        self.assertEqual(genome.get_connections_amount(), 1)
        # TODO: genome.remove_connection(connection)
        return

    def test_distance_function_default_on_different_genomes(self):
        # Test distance between:
        # [0, X, 2, X, X]
        # [0, 1, X, 3, 4]
        # disjoint = 2, excess = 2, weight_difference (same weight) = 0.
        # distance = 4.
        neat = Neat(1, 5, 10)
        genome_a = neat.create_new_genome()
        genome_b = neat.create_new_genome()

        # Genome mutations.
        neat.create_connection(genome_a, 0, 1)  # inn. index 0.
        neat.create_connection(genome_b, 0, 1)  # inn. index 0.
        neat.create_connection(genome_b, 0, 2)  # inn. index 1.
        neat.create_connection(genome_a, 0, 3)  # inn. index 2.
        neat.create_connection(genome_b, 0, 4)  # inn. index 3.
        neat.create_connection(genome_b, 0, 5)  # inn. index 4.

        self.assertEqual(neat.calculate_distance(genome_a, genome_b), 4)

    def test_distance_function_default_on_same_genomes(self):
        # Test distance between:
        # [0, 1]
        # [0, 1]
        # disjoint = 0, excess = 0, weight_difference = 0.
        # distance = 0.
        neat = Neat(1, 3, 10)
        genome_a = neat.create_new_genome()
        genome_b = neat.create_new_genome()

        # Genome mutations.
        neat.create_connection(genome_a, 0, 1)
        neat.create_connection(genome_a, 0, 2)
        neat.create_connection(genome_b, 0, 1)
        neat.create_connection(genome_b, 0, 2)

        self.assertEqual(neat.calculate_distance(genome_a, genome_b), 0)

    def test_distance_function_overloaded_on_different_genomes(self):
        # Test distance between:
        # [0, X, 2, X, X]
        # [0, 1, X, 3, 4]
        # disjoint = 2, excess = 2, weight_difference (same weight) = 0.
        # distance = 5.
        neat = Neat(1, 5, 10, distance_coefficients={"c1": 2, "c2": 0.5, "c3": 4})
        genome_a = neat.create_new_genome()
        genome_b = neat.create_new_genome()

        # Genome mutations.
        neat.create_connection(genome_a, 0, 1)  # inn. index 0.
        neat.create_connection(genome_b, 0, 1)  # inn. index 0.
        neat.create_connection(genome_b, 0, 2)  # inn. index 1.
        neat.create_connection(genome_a, 0, 3)  # inn. index 2.
        neat.create_connection(genome_b, 0, 4)  # inn. index 3.
        neat.create_connection(genome_b, 0, 5)  # inn. index 4.

        self.assertEqual(neat.calculate_distance(genome_a, genome_b), 5)

    def test_distance_function_overloaded_on_different_genomes_different_weights(self):
        # Test distance between:
        # [0, X, 2, X, X]
        # [0, 1, X, 3, 4]
        # disjoint = 2, excess = 2, weight_difference = 0.1.
        # distance = 4.075.
        neat = Neat(1, 5, 10, distance_coefficients={"c1": 1.5, "c2": 0.5, "c3": 0.75})
        genome_a = neat.create_new_genome()
        genome_b = neat.create_new_genome()

        # Genome mutations.
        neat.create_connection(genome_a, 0, 1, weight=0.1)  # inn. index 0.
        neat.create_connection(genome_b, 0, 1, weight=0.2)  # inn. index 0.
        neat.create_connection(genome_b, 0, 2, weight=0.3)  # inn. index 1.
        neat.create_connection(genome_a, 0, 3, weight=0.4)  # inn. index 2.
        neat.create_connection(genome_b, 0, 4, weight=0.5)  # inn. index 3.
        neat.create_connection(genome_b, 0, 5, weight=0.6)  # inn. index 4.

        self.assertEqual(neat.calculate_distance(genome_a, genome_b), round(4.075, 3))

    def test_crossover(self):
        neat = Neat(3, 3, 10)
        genome_a = neat.create_new_genome()
        genome_b = neat.create_new_genome()
        genome_c = neat.crossover(genome_a, genome_b)
        self.assertEqual(genome_c, False)


if __name__ == "__main__":
    unittest.main()
