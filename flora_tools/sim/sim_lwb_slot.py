import flora_tools.lwb_slot as lwb_slot
import flora_tools.sim.sim_node as sim_node
from flora_tools.sim.sim_gloria_flood import SimGloriaFlood
from flora_tools.sim.sim_message import SimMessage, SimMessageType


class SimLWBSlot:
    def __init__(self, node: 'sim_node.SimNode', slot: 'lwb_slot.LWBSlot', callback, master: 'sim_node.SimNode' = None,
                 message=None):
        self.node = node
        self.slot = slot
        self.message = message
        self.callback = callback
        self.master = master

        self.power_increase = True
        self.update_timestamp = True

        if slot.type is lwb_slot.LWBSlotType.DATA:
            self.power_increase = False
            self.update_timestamp = False
        elif slot.type is lwb_slot.LWBSlotType.CONTENTION:
            self.update_timestamp = False

        SimGloriaFlood(self.node, self.slot.flood, self.finished_flood, init_tx_message=self.message,
                       power_increase=self.power_increase, update_timestamp=self.update_timestamp)

    def finished_flood(self, message: 'SimMessage'):
        if self.node.role is not sim_node.SimNodeRole.BASE:
            if self.slot.type in [lwb_slot.LWBSlotType.SYNC, lwb_slot.LWBSlotType.SLOT_SCHEDULE]:
                if message is not None and message.type in [SimMessageType.SYNC,
                                                            SimMessageType.SLOT_SCHEDULE]:
                    self.node.lwb.link_manager.upgrade_link(message.source, message.modulation, message.power_level)
                elif self.master is not None:
                    self.node.lwb.link_manager.downgrade_link(self.master)
            elif self.slot.type in [lwb_slot.LWBSlotType.ACK]:
                if message is not None and message.type in [SimMessageType.ACK]:
                    self.node.lwb.link_manager.acknowledge_link(message.source)

        else:
            if self.slot.type in [lwb_slot.LWBSlotType.CONTENTION]:
                if message is not None and message.type in [SimMessageType.STREAM_REQUEST,
                                                            SimMessageType.ROUND_REQUEST]:
                    self.node.lwb.link_manager.upgrade_link(message.source, message.modulation, message.power_level)
                    if message.modulation is self.node.lwb.link_manager.get_link(message.source)['modulation']:
                        self.node.lwb.link_manager.acknowledge_link(message.source)
            elif message is not None:
                self.node.lwb.link_manager.upgrade_link(message.source, message.modulation, message.power_level)

        self.callback(message)
