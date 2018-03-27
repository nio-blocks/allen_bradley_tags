from pycomm.ab_comm.clx import Driver as ClxDriver
from nio.block.base import Block, Signal
from nio.properties import VersionProperty, StringProperty, BoolProperty, \
                           Property


class ABTagServices(Block):

    version = VersionProperty('0.1.0')
    host = StringProperty(title='Host Address')
    tags = Property(title='Tags')
    write = BoolProperty(title='Write?', default=False)

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
            write = self.write(signal)
            if write:
                tag_list = self.tags(signal)
                if isinstance(tag_list, list):
                    for tag in tag_list:
                        if not isinstance(tag, tuple):
                            self._abort()
                else:
                    if not isinstance(tag_list, tuple):
                        self._abort()
                value = self.cnxn.write_tag(tag_list)
            else:
                value = self.cnxn.read_tag(self.tags(signal))
            output_signals.append(Signal({'value': value}))
        self.notify_signals(output_signals)

    def _abort(self):
        raise TypeError(
            'Tags to write must be given as a tuple of (name, value, type)')
