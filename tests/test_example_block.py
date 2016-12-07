from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..example_block import Example


class TestExample(NIOBlockTestCase):

    def test_process_signals(self):
        """Signals pass through block unmodified."""
        blk = Example()
        self.configure_block(blk, {})
        blk.start()
        blk.process_signals([Signal({"hello": "n.io"})])
        blk.stop()
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {"hello": "n.io"})
