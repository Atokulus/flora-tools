import pandas as pd

from flora_tools.radio_configuration import RadioConfiguration
from flora_tools.radio_math import RadioMath

from flora_tools.sim.sim_message import SimMessage
import flora_tools.sim.sim_network as sim_network
import flora_tools.sim.sim_node as sim_node
from flora_tools.lwb_slot import POWERS

from copy import copy


class SimMessageManager:
    def __init__(self, network: 'sim_network.SimNetwork'):
        self.network = network
        self.mq = pd.DataFrame(columns=['source', 'modulation', 'band', 'power', 'tx_start', 'tx_end', 'message'])

    def tx_message(self, source: 'sim_node.SimNode', modulation, band, power, message: SimMessage):
        power = POWERS[power]
        config = RadioConfiguration(modulation, band, power, tx=True, preamble=(2 if modulation > 7 else 3))
        math = RadioMath(config)
        message.tx_end = message.timestamp + math.get_message_toa(payload_size=message.payload)

        message = copy(message)
        message.hop_count += 1

        self.mq.loc[len(self.mq)] = [source, modulation, band, power,
                                     source.transform_local_to_global_timestamp(message.timestamp),
                                     source.transform_local_to_global_timestamp(message.tx_end), message]
