from collections import defaultdict
from nio.util.support.block_test_case import NIOBlockTestCase


class TestExample(NIOBlockTestCase):

    def setUp(self):
        super().setUp()
        # This will keep a list of signals notified for each output
        self.last_notified = defaultdict(list)

    def signals_notified(self, signals, output_id='default'):
        self.last_notified[output_id].extend(signals)

    def test_pass(self):
        pass
