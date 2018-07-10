import abc

from flora_tools.sim.sim_message import SimMessage
from flora_tools.sim.sim_node import SimNode
from flora_tools.sim.stream import DataStream, NotificationStream


class Service:
    __metaclass__ = abc.ABCMeta

    def __init__(self, node: 'SimNode', name=None):
        self.node = node
        self.name = name

    @abc.abstractmethod
    def get_data(self) -> SimMessage:
        return

    @abc.abstractmethod
    def data_available(self) -> SimMessage:
        return

    @abc.abstractmethod
    def get_notification(self) -> SimMessage:
        return

    @abc.abstractmethod
    def notification_available(self) -> SimMessage:
        return

    @abc.abstractmethod
    def failed_datastream_callback(self, datastream: DataStream):
        return

    @abc.abstractmethod
    def failed_notification_callback(self, notification_stream: NotificationStream):
        return
