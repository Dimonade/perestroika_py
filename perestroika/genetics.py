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
tovarisches_in_sight = []
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
        source: int,
        target: int,
        weight: float = 1.0,
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
        self.nodes = {}
        self.connections = {}
        return

    def get_nodes_amount(self):
        return len(self.nodes)

    def get_connections_amount(self):
        return len(self.connections)

    def add_node(self, node: NodeGene):
        self.nodes.update({node.index: node})
        return

    def add_connection(self, connection: ConnectionGene):
        self.connections.update({connection.innovation_index: connection})
        return

    def remove_connection(self, connection: ConnectionGene):
        raise NotImplementedError
        self.connections.remove(connection)
        return

    def sort_connections(self):
        self.connections.sort(key=lambda k: k.innovation_index)
        return

    def print_nodes(self):
        for node in self.nodes:
            print(node.__dict__)
        return

    def print_connections(self):
        for connection in self.connections:
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
    def __init__(
        self,
        input_size: int,
        output_size: int,
        clients: int,
        distance_coefficients: dict = {"c1": 1, "c2": 1, "c3": 1},
    ):
        self.input_size = input_size
        self.output_size = output_size
        self.clients = clients
        self.distance_coefficients = distance_coefficients
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

    def create_connection(self, genome: Genome, source: int, target: int, weight: float = 1.0):
        connection_hash = f"{source:{hash_size}}" + f"{target:{hash_size}}"
        # Assume new connection.
        innovation_index = len(self.connections)

        if connection_hash not in self.connections.keys():
            self.connections.update({connection_hash: innovation_index})
        else:
            innovation_index = self.connections[connection_hash]

        genome.add_connection(ConnectionGene(innovation_index, source, target, weight))
        return

    def print_connections(self):
        for i, (key, value) in enumerate(self.connections.items()):
            print(key, value)
        return

    def calculate_distance(self, genome_a: Genome, genome_b: Genome):
        innovations_a = [
            a.innovation_index for a in genome_a.connections.values()
        ]
        innovations_b = [
            b.innovation_index for b in genome_b.connections.values()
        ]
        low_innovation = min(max(innovations_a), max(innovations_b))
        different = sorted(set(innovations_a) ^ set(innovations_b))
        excess = len([d for d in different if d > low_innovation])
        disjoint = len(different) - excess
        same_innovations = sorted(set(innovations_a) & set(innovations_b))
        similar = len(same_innovations)

        weight_difference = (
            sum(
                [
                    abs(
                        genome_a.connections[i].weight
                        - genome_b.connections[i].weight
                    )
                    for i in same_innovations
                ]
            )
            / similar
            )
        n = max(
            len(genome_a.connections), len(genome_b.connections)
        )
        if n < 20:
            n = 1

        d = (
            self.distance_coefficients["c1"] * excess / n
            + self.distance_coefficients["c2"] * disjoint / n
            + self.distance_coefficients["c3"] * weight_difference
        )

        return d

    def crossover(self, genome_a: Genome, genome_b: Genome) -> Genome:
        # TODO: Each connection with the same innovation number:
        #   randomly choose between the two parents (can inherit different
        # `weight` and `enabled`);
        # If only one parent has it: add it to the child as it is.
        # If the fitter parent has excess genes: add them to the child.
        genome_c = self.create_new_genome()
        return genome_c

    def mutate_add_node(self, genome: Genome):
        # Add a node on a connection so that:
        # src -> 1 -> new_node -> old_weight -> target.
        # (in practice: creates two new connections, and the old one is
        # removed, or deactivated).
        return

    def mutate_remove_connection(self, genome: Genome):
        return

    def mutate_add_connection(self, genome: Genome):
        return

    def mutate_remove_node(self, genome: Genome):
        return

    def mutate_enable_disable_connection(self, genome: Genome):
        # If connection is enabled -> disable and vice versa.
        return

    def mutate_weight_shift(self, genome: Genome):
        return

    def mutate_weight_random(self, genome: Genome):
        return

    def plot_genome(self, genome: Genome):
        return
