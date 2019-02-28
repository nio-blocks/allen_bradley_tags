from pycomm.ab_comm.clx import Driver as ClxDriver
from nio.block.base import Block, Signal
from nio.block.mixins import EnrichSignals, Retry

from nio.properties import VersionProperty, StringProperty, Property


class WriteTag(EnrichSignals, Retry, Block):

    version = VersionProperty("0.1.2")
    host = StringProperty(title='Host Address')
    tags = Property(title='Tags')

    def __init__(self):
        super().__init__()
        self.cnxn = ClxDriver()

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
                msg = 'Not connected to {}, reconnecting...'.format(host)
                self.logger.warning(msg)
                self._connect()
            except Exception:
                self.cnxn = None
                msg = 'Unable to connect to {}'.format(host)
                self.logger.exception(msg)
                return
        for signal in signals:
            tag_list = self.tags(signal)
            self._validate_tags(tag_list)
            try:
                response = self.execute_with_retry(
                    self._make_request, tag_list)
            except Exception:
                response = False
                self.cnxn = None
                msg = 'write_tag failed, host: {}, tags: {}'
                self.logger.exception(msg.format(host, tag_list))
                continue
            new_signal_dict = self._parse_response(response)
            new_signal_dict['host'] = host
            new_signal = self.get_output_signal(new_signal_dict, signal)
            output_signals.append(new_signal)
        self.notify_signals(output_signals)

    def _abort(self):
        raise TypeError(
            'Tags to write must be given as a tuple of (name, value, type)')

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

    def _make_request(self, tag_list):
        return self.cnxn.write_tag(tag_list)

    def _parse_response(self, response):
        if isinstance(response, list):
            # when writing multiple tags write_tag returns a list of
            # tuples (name, value, type, "GOOD"|"BAD")
            success = []
            for resp in response:
                success.append(resp[3] == "GOOD")
        else:
            success = response
        return {'success': success}

    def _validate_tags(self, tag_list):
        if isinstance(tag_list, list):
            for tag in tag_list:
                if not isinstance(tag, tuple):
                    self._abort()
        else:
            if not isinstance(tag_list, tuple):
                self._abort()
