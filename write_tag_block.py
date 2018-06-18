from pycomm.ab_comm.clx import Driver as ClxDriver
from nio.block.base import Block, Signal
from nio.block.mixins.enrich.enrich_signals import EnrichSignals

from nio.properties import VersionProperty, StringProperty, Property


class WriteTag(EnrichSignals, Block):

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
            tag_list = self.tags(signal)
            if isinstance(tag_list, list):
                for tag in tag_list:
                    if not isinstance(tag, tuple):
                        self._abort()
            else:
                if not isinstance(tag_list, tuple):
                    self._abort()
            response = self.cnxn.write_tag(tag_list)
            if isinstance(response, list):
                # when writing multiple tags write_tag returns a list of
                # tuples (name, value, type, "GOOD"|"BAD")
                success = []
                for resp in response:
                    success.append(resp[3] == "GOOD")
            else:
                success = response
            new_signal = self.get_output_signal({'success': success}, signal)
            output_signals.append(new_signal)
        self.notify_signals(output_signals)

    def _abort(self):
        raise TypeError(
            'Tags to write must be given as a tuple of (name, value, type)')
