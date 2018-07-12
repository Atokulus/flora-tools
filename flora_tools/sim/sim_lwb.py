from enum import Enum

import numpy as np

import flora_tools.sim.sim_node as sim_node
from flora_tools.sim.lwb_schedule_manager import LWBScheduleManager
from flora_tools.sim.sim_cad_sync import SimCADSync
from flora_tools.sim.sim_link_manager import LWBLinkManager
from flora_tools.sim.stream import LWBStreamManager


SYNC_PERIOD = 1 / 8E6 * np.exp2(31)  # 268.435456 s


class LWBState(Enum):
    CAD = 1
    ASSIGNED = 2


class SimLWB:
    def __init__(self, node: 'sim_node.SimNode'):
        self.node = node

        self.rounds = []

        self.link_manager = LWBLinkManager(self)
        self.stream_manager = LWBStreamManager(self)
        self.schedule_manager = LWBScheduleManager(self.node)
        self.state: LWBState = LWBState.CAD

        if self.node.role is sim_node.SimNodeRole.BASE:
            self.base = self.node
        else:
            self.base = None
            self.state: LWBState = LWBState.CAD

    def run(self):
        if self.state is LWBState.CAD:
            self.sync = SimCADSync(self.node)
            self.sync.run(self.sync_callback)
        elif self.state is LWBState.ASSIGNED:
            self.schedule_manager.get_round()

    def sync_callback(self):
        self.state = LWBState.ASSIGNED
