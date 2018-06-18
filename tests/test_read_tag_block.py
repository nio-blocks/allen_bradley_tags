from unittest.mock import patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..read_tag_block import ReadTag


class TestReadTag(NIOBlockTestCase):

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_read_tag(self, mock_clx):
        """A tag is read is its value notified"""
        # if passes only a string, read_tag returns (value, type)
        tag = 'foo'
        mock_read_values = (3.14, 'REAL')
        mock_clx.return_value.read_tag.return_value = mock_read_values
        blk = ReadTag()
        self.configure_block(blk, {'host': 'ip_addr', 'tags': '{{ $tag }}'})
        blk.start()
        blk.process_signals([Signal({'tag': tag})])
        blk.stop()
        mock_clx.return_value.open.assert_called_once_with('ip_addr')
        mock_clx.return_value.close.assert_called_once_with()
        mock_clx.return_value.read_tag.assert_called_once_with(tag)
        self.assert_num_signals_notified(1)
        # we add the tag name to the returned value
        expected_value = (tag,) + mock_read_values
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'value': expected_value})

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_read_multiple_tags(self, mock_clx):
        """A list of tags is read, notifying a list of values"""
        # read_tag returns a list of tuples of (name, value, type)
        tags = ['foo', 'bar', 'baz']
        tag_expr = '{{' + '[\'{}\', \'{}\', \'{}\']'.format(*tags) + '}}'
        mock_read_values = [
            (tags[0], 0, 'INT'), (tags[1], 1, 'DINT'), (tags[2], 2.0, 'REAL')]
        mock_clx.return_value.read_tag.return_value = mock_read_values
        blk = ReadTag()
        self.configure_block(
            blk, {'host': 'ip_addr',
                  'tags': tag_expr})
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        mock_clx.return_value.read_tag.assert_called_once_with(tags)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'value': mock_read_values})

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_signal_lists(self, mock_clx):
        """Outgoing signal lists are the same length as input"""
        blk = ReadTag()
        self.configure_block(blk, {'host': 'ip_addr', 'tags': 'foo'})
        blk.start()
        blk.process_signals([Signal(), Signal()])
        blk.stop()
        self.assertEqual(2, len(self.notified_signals[DEFAULT_TERMINAL][-1]))

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_signal_enrichment(self, mock_clx):
        """Block mixin is implemented correctly"""
        tag = 'foo'
        mock_read_values = (1, 'INT')
        mock_clx.return_value.read_tag.return_value = mock_read_values
        blk = ReadTag()
        self.configure_block(blk, {'host': 'ip_addr',
                                   'tags': tag,
                                   'enrich': {'exclude_existing': False}})
        blk.start()
        blk.process_signals([Signal({'pi': 3.14})])
        blk.stop()
        expected_value = (tag,) + mock_read_values
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'value': expected_value, 'pi': 3.14})
