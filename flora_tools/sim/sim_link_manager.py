import pandas as pd

import flora_tools.lwb_slot as lwb_slot
import flora_tools.sim.sim_node as sim_node


class SimLinkManager:
    def __init__(self, node: 'sim_node.SimNode'):
        self.node = node

        self.links = pd.DataFrame(columns=['modulation', 'power', 'counter'])
        self.links.index.name = 'id'

    def upgrade_link(self, target_node: 'sim_node.SimNode', modulation: int, power_level: int):
        current_link = self.links[target_node.id]

        if modulation > current_link['modulation'] or (
                modulation == current_link['modulation'] and power_level < current_link['power']):
            if current_link['counter'] == 0:
                self.links[target_node.id] = [modulation, power_level, 1]
            else:
                self.links.loc[target_node.id, 'counter'] -= 1

    def downgrade_link(self, target_node: 'sim_node.SimNode'):
        self.links[target_node.id, 'counter'] += 1
        if self.links[target_node.id, 'counter'] > 1:
            if self.links[target_node.id, 'power'] < len(lwb_slot.POWERS) - 1:
                self.links[target_node.id] = [self.links[target_node.id, 'modulation'],
                                              self.links[target_node.id, 'power'] + 1, 1]
            else:
                if self.links[target_node.id, 'modulation'] < len(lwb_slot.MODULATIONS) - 1:
                    self.links[target_node.id] = [self.links[target_node.id, 'modulation'] + 1,
                                                  self.links[target_node.id, 'power'] + 1, 1]
                else:
                    self.links.drop(id)
