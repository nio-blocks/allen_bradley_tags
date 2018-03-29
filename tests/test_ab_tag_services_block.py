from unittest.mock import patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..ab_tag_services_block import ABTagServices


class TestABTagServices(NIOBlockTestCase):

    @patch(ABTagServices.__module__ + '.ClxDriver')
    def test_read_tag(self, mock_clx):
        mock_clx.return_value.read_tag.return_value = 'bar'
        blk = ABTagServices()
        self.configure_block(blk, {'host': 'ip_addr', 'tags': '{{ $tag }}'})
        blk.start()
        blk.process_signals([Signal({'tag': 'foo'})])
        blk.stop()
        mock_clx.return_value.open.assert_called_once_with('ip_addr')
        mock_clx.return_value.close.assert_called_once_with()
        mock_clx.return_value.read_tag.assert_called_once_with('foo')
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'value': 'bar'})

    @patch(ABTagServices.__module__ + '.ClxDriver')
    def test_read_multiple_tags(self, mock_clx):
        mock_clx.return_value.read_tag.return_value = ['oof', 'rab', 'zab']
        blk = ABTagServices()
        self.configure_block(
            blk,
            {'host': 'ip_addr', 'tags': '{{ [\'foo\', \'bar\', \'baz\'] }}'})
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        mock_clx.return_value.read_tag.assert_called_once_with(
            ['foo', 'bar', 'baz'])
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'value': ['oof', 'rab', 'zab']})

    @patch(ABTagServices.__module__ + '.ClxDriver')
    def test_write_tag(self, mock_clx):
        tag_to_write = ('seven', 7, 'INT')
        tag_expr = '{{ (\'seven\', 7, \'INT\') }}'
        mock_clx.return_value.write_tag.return_value = tag_to_write
        blk = ABTagServices()
        self.configure_block(
            blk,
            {'host': 'ip_addr', 'tags': tag_expr, 'write': '{{ $write }}'})
        blk.start()
        blk.process_signals([Signal({'write': True})])
        blk.stop()
        mock_clx.return_value.write_tag.assert_called_once_with(tag_to_write)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'value': ('seven', 7, 'INT')})

    @patch(ABTagServices.__module__ + '.ClxDriver')
    def test_write_invalid_tag(self, mock_clx):
        blk = ABTagServices()
        self.configure_block(
            blk,
            {'host': 'ip_addr', 'tags': 'not a tuple', 'write': True})
        blk.start()
        with self.assertRaises(TypeError):
            blk.process_signals([Signal()])
        blk.stop()

    @patch(ABTagServices.__module__ + '.ClxDriver')
    def test_write_tags_one_invalid(self, mock_clx):
        tag_expr = '{{ [\'not a tuple\', (\'seven\', 7, \'INT\')] }}'
        blk = ABTagServices()
        self.configure_block(
            blk,
            {'host': 'ip_addr', 'tags': tag_expr, 'write': True})
        blk.start()
        with self.assertRaises(TypeError):
            blk.process_signals([Signal()])
        blk.stop()

    @patch(ABTagServices.__module__ + '.ClxDriver')
    def test_signal_lists(self, mock_clx):
        mock_clx.return_value.read_tag.side_effect = ['foo', 'bar']
        blk = ABTagServices()
        self.configure_block(blk, {'host': 'ip_addr', 'tags': '{{ $tag }}'})
        blk.start()
        blk.process_signals([Signal({'tag': 'foo'}), Signal({'tag': 'bar'})])
        blk.stop()
        self.assert_signal_list_notified(
            [Signal({'value': 'foo'}), Signal({'value': 'bar'})])
