from pycomm.ab_comm.clx import Driver as ClxDriver
from nio.block.base import Block, Signal
from nio.block.mixins.enrich.enrich_signals import EnrichSignals
from nio.properties import VersionProperty, StringProperty, Property


class ReadTag(EnrichSignals, Block):

    version = VersionProperty('0.1.0')
    host = StringProperty(title='Host Address')
    tags = Property(title='Tags')

    def __init__(self):
        super().__init__()
        self.cnxn = ClxDriver()

    def configure(self, context):
        super().configure(context)
        self.cnxn.open(self.host())

    def stop(self):
        super().stop()
        self.cnxn.close()

    def process_signals(self, signals):
        output_signals = []
        for signal in signals:
            value = self.cnxn.read_tag(self.tags(signal))
            if not isinstance(value[0], tuple):
                # read_tag only includes the tag's name in the return value
                # when reading a list of tags, so we include it here
                value = (self.tags(signal),) + value
            new_signal = self.get_output_signal({'value': value}, signal)
            output_signals.append(new_signal)
        self.notify_signals(output_signals)
