from typing import Callable

import numpy as np
import pandas as pd

from flora_tools.sim.sim_network import SimNetwork
from flora_tools.sim.sim_node import SimNode
from enum import Enum


class SimEventType(Enum):
    TX_DONE = 1
    RX_TIMEOUT = 2
    RX_DONE = 3
    UPDATE = 4


class SimEventManager:
    def __init__(self, network: 'SimNetwork'):
        self.network = network
        self.eq = pd.DataFrame(columns=['timestamp', 'local_timestamp', 'node', 'type', 'data', 'callback'])

    def loop(self, iterations=1):
        for i in range(iterations):
            self.eq = self.eq.sort_values(by=['timestamp'])
            event = self.eq[self.eq.timestamp >= self.network.current_timestamp].iloc[0, :]
            self.process_event(event)
            self.network.current_timestamp = event['timestamp']
            event['node'].local_timestamp = event['local_timestamp']

    @staticmethod
    def process_event(event):
        event['callback'](event)

    def register_event(self, timestamp: float, node: 'SimNode', type: SimEventType, callback: Callable[[None], None], content=None):
        self.eq.loc[len(self.eq)] = [node.transform_local_to_global_timestamp(timestamp), timestamp, node, type, content, callback]
