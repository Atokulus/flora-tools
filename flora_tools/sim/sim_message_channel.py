import numpy as np
import pandas as pd

from flora_tools.sim.sim_message import SimMessage
from flora_tools.sim.sim_node import SimNode

from flora_tools.gloria_math import GloriaMath
from flora_tools.radio_configuration import RadioConfiguration
from flora_tools.radio_math import RadioMath, RADIO_SNR


class SimMessageChannel:
    def __init__(self, network):
        self.network = network
        self.mm = network.mm

    def get_potential_rx_message(self, modulation, band, rx_node: 'SimNode', rx_start, rx_timeout=None) -> SimMessage:

        rx_start = rx_node.transform_local_to_global_timestamp(rx_start)


        def mark_reachable_message(item):
            return self.network.is_reachable(rx_node, self.network.nodes[item.source], power=item.power)

        def calc_power_message(item):
            return self.network.calculate_path_loss(rx_node, self.network.nodes[item.source])

        config = RadioConfiguration(modulation, preamble=GloriaMath().preamble_len(modulation))
        math = RadioMath(config)

        valid_rx_start = rx_start + math.get_symbol_time() * 0.1
        keep_quiet_start = rx_start - 100E-6

        interfering_set = (self.mm.mq.loc[
            self.modulation == band &
            self.mm.mq.tx_end >= keep_quiet_start &
            self.mm.mq.tx_start <= valid_rx_start
        ]).copy()

        if rx_timeout is None:
            rx_timeout = rx_start + math.get_preamble_time()

        subset = (self.mm.mq.loc[
            self.mm.mq.modulation == modulation &
            self.mm.mq.band == band &
            self.mm.mq.tx_start >= valid_rx_start &
            self.mm.mq.tx_start <= rx_timeout
        ]).copy()

        subset['reachable'] = subset.applymap(mark_reachable_message, axis=1)
        subset = subset.loc[subset.reachable == True]

        if len(subset) > 0:
            interfering_set['rx_power'] = interfering_set.applymap(calc_power_message, axis=1)
            subset['rx_power'] = calc_power_message(subset)

            interfering_power = 0
            for i in interfering_set.rx_power:
                interfering_power += np.pow(10, i/10)

            candidates = []
            for i in subset.sort_values(by=['rx_power'], ascending=False):
                if np.pow(10, i.rx_power / 10) > (interfering_power + np.pow(10, RADIO_SNR[modulation])):
                    candidates.append(i)

            if len(candidates > 0):
                return candidates[0]
            else:
                return None
        else:
            return None

    def check_if_successfully_received(self, modulation, band, potential_message, rx_start, rx_node):
        rx_start = rx_node.transform_local_to_global_timestamp(rx_start)

        def calc_power_message(item):
            return self.network.calculate_path_loss(rx_node, self.network.nodes[item.node_id])

        config = RadioConfiguration(modulation, preamble=GloriaMath().preamble_len(modulation))
        math = RadioMath(config)
        valid_rx_start = rx_start + math.get_symbol_time() * 0.5

        tx_start = potential_message.tx_start
        tx_end = tx_start + potential_message.time

        interfering_set = (self.mm.mq.loc[
            self.mm.mq.modulation == modulation &
            self.mm.mq.band == band & self.mm.mq.event_type == 'tx' &
            self.mm.mq.tx_end >= rx_start &
            self.mm.mq.tx_start <= potential_message.tx_end &
            (
                    self.mm.mq.message_id != potential_message.id |
                    (self.mm.mq.message_id == potential_message.id &
                     self.mm.mq.tx_start > potential_message.tx_start &
                     self.mm.mq.tx_start <= potential_message.tx_end)
            )
            ]).copy()

        interfering_set['rx_power'] = interfering_set.applymap(calc_power_message, axis=1)
        potential_message['rx_power'] = calc_power_message(potential_message)

        interfering_power = 0
        for i in interfering_set.rx_power:
            interfering_power += np.pow(10, i / 10)

        if np.pow(10, potential_message.rx_power / 10) > (interfering_power + np.pow(10, RADIO_SNR[modulation])):
            return True
        else:
            return False

    def calculate_path_loss(self, node_a, node_b):
        return self.network.G[node_a.id, node_b.id]['path_loss']

    def is_reachable(self, modulation, node_a, node_b, power=22):
        config = RadioConfiguration(modulation)
        math = RadioMath(config)
        pl = self.calculate_path_loss(node_a, node_b)
        if pl <= -math.link_budget(power=power):
            return True
        else:
            return False


    def cad_result(self, timestamp, rx_node: 'SimNode', modulation, band):
        timestamp = rx_node.transform_local_to_global_timestamp(timestamp)

        def mark_reachable_message(item):
            return self.network.is_reachable(rx_node, self.network.nodes[item.source], power=item.power)

        def calc_power_message(item):
            return self.network.calculate_path_loss(rx_node, self.network.nodes[item.source])

        config = RadioConfiguration(modulation, preamble=GloriaMath().preamble_len(modulation))
        math = RadioMath(config)



        tx_start = potential_message.tx_start
        tx_end = tx_start + potential_message.time

        interfering_set = (self.mm.mq.loc[
            self.mm.mq.modulation == modulation &
            self.mm.mq.band == band & self.mm.mq.event_type == 'tx' &
            self.mm.mq.tx_end >= rx_start &
            self.mm.mq.tx_start <= potential_message.tx_end &
            (
                    self.mm.mq.message_id != potential_message.id |
                    (self.mm.mq.message_id == potential_message.id &
                     self.mm.mq.tx_start > potential_message.tx_start &
                     self.mm.mq.tx_start <= potential_message.tx_end)
            )
            ]).copy()

        interfering_set['rx_power'] = interfering_set.applymap(calc_power_message, axis=1)
        potential_message['rx_power'] = calc_power_message(potential_message)

        interfering_power = 0
        for i in interfering_set.rx_power:
            interfering_power += np.pow(10, i / 10)

        if np.pow(10, potential_message.rx_power / 10) > (interfering_power + np.pow(10, RADIO_SNR[modulation])):
            return True
        else:
            return False






