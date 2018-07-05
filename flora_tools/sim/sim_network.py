import numpy as np
import networkx as nx
from itertools import combinations
import matplotlib.pyplot as plt

from flora_tools.radio_configuration import RadioConfiguration
from flora_tools.radio_math import RadioMath

from flora_tools.sim.sim_node import SimNode
from flora_tools.sim.sim_message_manager import SimMessageManager
from flora_tools.sim.sim_event_manager import SimEventManager
from flora_tools.sim.sim_message_channel import SimMessageChannel


class SimNetwork:
    def __init__(self, count=10, path_loss=[110, 170], seed=None):
        self.current_timestamp = 0
        self.mm = SimMessageManager(self)
        self.mc = SimMessageChannel(self)
        self.em = SimEventManager(self)

        self.nodes = [SimNode(self, mm=self.mm, em=self.em, id=i, role='sensor', datarate=10) for i in range(count)]
        self.G = nx.Graph()
        self.G.add_nodes_from(range(count))

        edges = list(combinations(range(count), 2))

        np.random.seed(seed)
        path_losses = np.random.uniform(path_loss[0], path_loss[1], len(list(edges)))
        channels = [tuple([edge[0], edge[1], {'path_loss': path_losses[index]}]) for index, edge in enumerate(edges)]

        self.G.add_edges_from(channels)
    def draw(self, modulation=None):
        if modulation is not None:
            H = self.G.copy()
            config = RadioConfiguration(modulation)
            math = RadioMath(config)
            edges_to_remove = []
            for (u, v, pl) in H.edges.data('path_loss'):
                if pl > -math.link_budget():
                    edges_to_remove.append((u, v))

            H.remove_edges_from(edges_to_remove)
            nx.draw(H, with_labels=True, font_weight='bold')
        else:
            nx.draw(self.G, with_labels=True, font_weight='bold')





