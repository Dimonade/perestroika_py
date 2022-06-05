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
        neat.create_connection(
            genome.genome["nodes"][0], genome.genome["nodes"][1], genome
        )
        self.assertEqual(genome.get_connections_amount(), 1)
        # TODO: genome.remove_connection(connection)
        return


if __name__ == "__main__":
    unittest.main()
