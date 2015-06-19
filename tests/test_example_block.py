from collections import defaultdict
from nio.common.signal.base import Signal
from nio.util.support.block_test_case import NIOBlockTestCase
from ..example_block import Example


class TestExample(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def test_pass(self):
        pass

    def test_process_signals(self):
        blk = Example()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(self.last_notified['default'][0].to_dict(), {})
