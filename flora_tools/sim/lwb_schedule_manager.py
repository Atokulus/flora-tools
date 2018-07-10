import numpy as np

import flora_tools.sim.sim_node as sim_node

sync_period = 1 / 8E6 * np.exp2(29)  # Sync every 67.108864 (~ 15 years of battery life)
schedule_granularity = sync_period / 256


class LWBScheduleManager:
    def __init__(self, node: 'sim_node.SimNode'):
        self.node = node

        self.rounds = []

        if self.node.role is 'base':
            self.base = self.node
            self.generate_initial_schedule()
        else:
            self.base = None

    def generate_initial_schedule(self):
        slot_times = LWBVisualizer.calculate_sync_round(lwb_math.modulations[0], self.node.local_timestamp, self.node)

        self.rounds.append({'offsets': slot_times, 'master': self.node})

        end_of_last_round = slot_times[-1]['offset']

        for i in reversed(range(len(lwb_math.modulations))):
            slots = [{'type': 'contention_slot'} for x in range(lwb_math.initial_contention_layout[i])]
            slot_times = LWBVisualizer.calculate_round(lwb_math.modulations[i], slots, self.node)

            for offset in slot_times:
                offset['offset'] += end_of_last_round

            self.rounds.append({'modulation': lwb_math.modulations[i], 'offsets': slot_times, 'master': self.node})

            end_of_last_round = slot_times[-1]['offset']

        self.schedule = slot_times

    def select_data_slot_message(self):
        pass
