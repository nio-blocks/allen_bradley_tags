from pycomm.ab_comm.clx import Driver as ClxDriver
from nio.block.base import Block, Signal
from nio.block.mixins import EnrichSignals, Retry
from nio.properties import VersionProperty, StringProperty, Property


class ReadTag(EnrichSignals, Retry, Block):

    host = StringProperty(title='Host Address', order=0)
    tags = Property(title='Tags', order=1)
    version = VersionProperty('0.2.0')

    def __init__(self):
        super().__init__()
        self.cnxn = None

    def before_retry(self, *args, **kwargs):
        self._disconnect()
        self._connect()

    def configure(self, context):
        super().configure(context)
        try:
            self._connect()
        except Exception:
            self.cnxn = None
            msg = 'Unable to connect to {}'.format(self.host())
            self.logger.exception(msg)

    def stop(self):
        super().stop()
        self._disconnect()

    def process_signals(self, signals):
        host = self.host()
        output_signals = []
        if self.cnxn is None:
            try:
                msg = 'Connecting to {}'.format(host)
                self.logger.warning(msg)
                self._connect()
            except Exception as exc:
                self.cnxn = None
                msg = 'Unable to connect to {}'.format(host)
                self.logger.error(msg)
                raise exc
        for signal in signals:
            tag = self.tags(signal)
            try:
                value = self.execute_with_retry(self._make_request, tag)
            except Exception as exc:
                value = False
                self.cnxn = None
                msg = 'read_tag failed, host: {}, tag: {}'
                self.logger.error(msg.format(host, tag))
                raise exc
            if value:
                if not isinstance(value[0], tuple):
                    # read_tag only includes the tag name in the return value
                    # when reading a list of tags, so we include it here
                    value = (tag, ) + value
                new_signal_dict = {'host': host, 'value': value}
                new_signal = self.get_output_signal(new_signal_dict, signal)
                output_signals.append(new_signal)
            else:
                msg = 'read_tag failed, host: {}, tag: {}'
                msg = msg.format(host, tag)
                self.logger.error(msg)
                    
        self.notify_signals(output_signals)

    def _connect(self):
        # each instance of ClxDriver can open connection to only 1 host
        # subsequent calls to open() are quietly ignored, and close()
        # does not take any args, so one host per block instance for now
        self.cnxn = ClxDriver()
        self.cnxn.open(self.host())

    def _disconnect(self):
        if self.cnxn is not None:
            self.cnxn.close()
            self.cnxn = None

    def _make_request(self, tag):
        return self.cnxn.read_tag(tag)
