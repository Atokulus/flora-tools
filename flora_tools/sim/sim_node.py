from enum import Enum

from flora_tools.sim.sensor_service import SensorService
from flora_tools.sim.sim_event_manager import SimEventManager
from flora_tools.sim.sim_lwb_manager import SimLWBManager
from flora_tools.sim.sim_message_manager import SimMessageManager
from flora_tools.sim.sim_network import SimNetwork


class SimNodeRole(Enum):
    BASE = 1
    RELAY = 2
    SENSOR = 3


class SimNode:
    def __init__(self, network: 'SimNetwork', em: SimEventManager, mm: SimMessageManager, id: int = None,
                 role: SimNodeRole = SimNodeRole.SENSOR):
        self.state = 'init'
        self.network = network
        self.mm = mm
        self.em = em
        self.id = id
        self.role = role

        self.lwb_manager = SimLWBManager(self)

        self.local_timestamp = 0

        if self.role is 'sensor':
            service = SensorService(self, "sensor_data{}".format(self.id), 10)
            self.lwb_manager.stream_manager.register_data(service.datastream)

        self.lwb_manager.run()

    def __str__(self):
        return str(self.id)

    def transform_local_to_global_timestamp(self, timestamp):
        timestamp - self.local_timestamp + self.network.current_timestamp
