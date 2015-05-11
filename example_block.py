from nio.common.block.base import Block
from nio.common.discovery import Discoverable, DiscoverableType


@Discoverable(DiscoverableType.block)
class Example(Block):

    """ This is the Example block. Put a brief description here. """

    def process_signals(self, signals, input_id='default'):
        pass
