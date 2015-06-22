from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType
from nio.metadata.properties import VersionProperty


@Discoverable(DiscoverableType.block)
class Example(Block):

    """ This is the Example block. Put a brief description here. """

    version = VersionProperty('0.1.0')

    def process_signals(self, signals, input_id='default'):
        for signal in signals:
            pass
        self.notify_signals(signals, output_id='default')
