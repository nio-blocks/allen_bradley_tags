from nio.block.base import Block
from nio.util.discovery import discoverable
from nio.properties import VersionProperty


@discoverable
class Example(Block):

    version = VersionProperty('0.1.0')

    def process_signals(self, signals):
        for signal in signals:
            pass
        self.notify_signals(signals)
