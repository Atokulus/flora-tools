from flora_tools.sim.sim_message import SimMessage
from flora_tools.sim.sim_lwb_slot_manager import SimLWBSlotManager
from flora_tools.sim.sim_node import SimNode
import flora_tools.lwb_math as lwb_math
from flora_tools.lwb_math import LWBMath

class LWBScheduleManager:
    def __init__(self, node: 'SimNode'):
        self.node = node

        self.rounds = []

        if self.node.role is 'base':
            self.base = self.node
            self.generate_initial_schedule()
        else:
            self.base = None

    def generate_initial_schedule(self):
        slot_times = LWBMath.calculate_sync_round(lwb_math.modulations[0], self.node.local_timestamp, self.node)

        self.rounds.append({'offsets': slot_times, 'master': self.node})

        end_of_last_round = slot_times[-1]['offset']

        for i in reversed(range(len(lwb_math.modulations))):
            slots = [{'type': 'contention_slot'} for x in range(lwb_math.initial_contention_layout[i])]
            slot_times = LWBMath.calculate_round(lwb_math.modulations[i], slots, self.node)

            for offset in slot_times:
                offset['offset'] += end_of_last_round

            self.rounds.append({'modulation': lwb_math.modulations[i], 'offsets': slot_times, 'master': self.node})

            end_of_last_round = slot_times[-1]['offset']

        self.schedule = slot_times

    def select_data_slot_message(self):
        pass

