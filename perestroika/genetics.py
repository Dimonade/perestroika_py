import copy
import matplotlib
import os

# NEAT consts.
max_nodes = 100
hash_size = f"0{len(str(max_nodes))}"
max_connections = 100**2

# Field characteristics.
height = 10
width = 10
force_field = (1, 1)
drag = 0
visible_light_intensity = 1
visible_light_direction = (0, 0)
uv_light_intensity = 1
uv_light_direction = (0, 0)
salinity = 0
ph = 7

# Tovarisch characteristics.
health = 1
age = 0
body_parts = []
mutation_rate = 0
hunger = 0
energy = 0
genome = 0  # Genome
visible_light_sight_distance = 1
visible_light_sight_angle = 90
uv_light_sight_distance = 1
uv_light_sight_angle = 90
kamtans_in_sight = []
immune_system = 0


# actions
accelerate = 0
rotate = 0
breed = 0
consume = 0
grab = 0
digest = 0
produce_pheromone = 0
grow = 0
attack = 0


# Neural stuff.
activation_functions = [
    "identity",
    "binary",
    "gelu",
    "softplus",
    "elu",
    "selu",
    "prelu",
    "silu",
    "gaussian",
    "gcu",
    "tanh",
    "relu",
    "sigmoid",
]


class NodeGene:
    def __init__(self, index: int, x=None, y=None):
        self.index = index
        self.x = x
        self.y = y
        self.gene_type: str = "node_gene"
        return


class ConnectionGene:
    def __init__(
        self,
        innovation_index: int,
        source: NodeGene,
        target: NodeGene,
        weight: float,
        enabled: bool = True,
    ):
        self.innovation_index = innovation_index
        self.source = source
        self.target = target
        self.weight = weight
        self.enabled = enabled
        self.gene_type: str = "connection_gene"


class Genome:
    def __init__(self):
        self.genome = {"nodes": [], "connections": []}
        return

    def get_nodes_amount(self):
        return len(self.genome["nodes"])

    def get_connections_amount(self):
        return len(self.genome["connections"])

    def add_node(self, node: NodeGene):
        self.genome["nodes"].append(node)
        return

    def add_connection(self, connection: ConnectionGene):
        self.genome["connections"].append(connection)
        return

    def remove_connection(self, connection: ConnectionGene):
        self.genome["connections"].remove(connection)
        return

    def sort_connections(self):
        self.genome["connections"].sort(key=lambda k: k.innovation_index)
        return

    def print_nodes(self):
        for node in self.genome["nodes"]:
            print(node.__dict__)
        return

    def print_connections(self):
        for connection in self.genome["connections"]:
            print(connection.__dict__)
        return

    def print_genome(self):
        self.print_nodes()
        self.print_connections()
        return

    def crossover(self, genome_a, genome_b):
        return

    def mutate(self):
        return


class Neat:
    def __init__(self, input_size: int, output_size: int, clients: int):
        self.input_size = input_size
        self.output_size = output_size
        self.clients = clients
        self.connections = {}
        return

    def create_new_genome(self) -> Genome:
        genome = Genome()

        for i in range(self.input_size):
            in_gene = NodeGene(i, 0.1, round((i + 1) / (self.input_size + 1), 3))
            genome.add_node(in_gene)
        for o in range(self.output_size):
            out_gene = NodeGene(
                self.input_size + o, 0.9, round((o + 1) / (self.output_size + 1), 3)
            )
            genome.add_node(out_gene)
        return genome

    def create_connection(self, source: NodeGene, target: NodeGene, genome: Genome):
        connection_hash = f"{source.index:{hash_size}}" + f"{target.index:{hash_size}}"
        # Assume new connection.
        innovation_index = len(self.connections)

        if connection_hash not in self.connections.keys():
            self.connections.update({connection_hash: innovation_index})
        else:
            innovation_index = self.connections[connection_hash]

        genome.add_connection(
            ConnectionGene(innovation_index, source.index, target.index, 1)
        )
        genome.sort_connections()
        return

    def print_connections(self):
        for i, (key, value) in enumerate(self.connections.items()):
            print(key, value)
        return

    def calculate_distance(self, connections_a: list, connections_b: list):
        disjoint = 0
        excess = 0
        weight_difference = 0
        similar = 0

        low_innovation = min(
            connections_a[0].innovation_index, connections_b[0].innovation_index
        )
        high_innovations = max(
            connections_a[-1].innovation_index, connections_b[-1].innovation_index
        )

        for (a, b) in zip(connections_a, connections_b):
            diff = abs(a.innovation_index - b.innovation_index)

            if diff:
                disjoint += diff
            pass

        return 0
