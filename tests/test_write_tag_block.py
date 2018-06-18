from unittest.mock import patch
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..write_tag_block import WriteTag


class TestWriteTag(NIOBlockTestCase):

    @patch(WriteTag.__module__ + '.ClxDriver')
    def test_write_tag(self, mock_clx):
        """A valid tag is written and successful status notified"""
        tag_to_write = ('seven', 7, 'INT')
        tag_expr = '{{ (\'seven\', 7, \'INT\') }}'
        # write_tag returns a bool indicating success
        mock_clx.return_value.write_tag.return_value = True
        blk = WriteTag()
        self.configure_block(blk, {'host': 'ip_addr', 'tags': tag_expr})
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        mock_clx.return_value.write_tag.assert_called_once_with(tag_to_write)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'success': True})

    @patch(WriteTag.__module__ + '.ClxDriver')
    def test_write_multiple_tags(self, mock_clx):
        """Multiple tags are written with varied success"""
        tags_to_write = [('seven', 7, 'INT'), ('pi', 3.14, 'REAL')]
        tag_expr = '{{ [(\'seven\', 7, \'INT\'), (\'pi\', 3.14, \'REAL\')] }}'
        # write_tag returns a list of tuples (name, value, type, "GOOD"|"BAD")
        mock_clx.return_value.write_tag.return_value = [
            ('seven', 7, 'INT', 'GOOD'),  ('pi', 3.14, 'REAL', 'BAD')]
        blk = WriteTag()
        self.configure_block(blk, {'host': 'ip_addr', 'tags': tag_expr})
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        mock_clx.return_value.write_tag.assert_called_once_with(tags_to_write)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'success': [True, False]})

    @patch(WriteTag.__module__ + '.ClxDriver')
    def test_write_invalid_tag(self, mock_clx):
        """Only write tags that are inside a valid tuple"""
        blk = WriteTag()
        self.configure_block(blk, {'host': 'ip_addr', 'tags': 'not a tuple'})
        blk.start()
        with self.assertRaises(TypeError):
            blk.process_signals([Signal()])
        self.assertEqual(mock_clx.return_value.write_tag.call_count, 0)
        blk.stop()

    @patch(WriteTag.__module__ + '.ClxDriver')
    def test_write_tags_one_invalid(self, mock_clx):
        """No tags are written if any of them are not a valid tuple"""
        tag_expr = '{{ [(\'seven\', 7, \'INT\'), \'not a tuple\'] }}'
        blk = WriteTag()
        self.configure_block(blk, {'host': 'ip_addr', 'tags': tag_expr})
        blk.start()
        with self.assertRaises(TypeError):
            blk.process_signals([Signal()])
        # if any tag in a list is invalid, no write_tag call is made
        self.assertEqual(mock_clx.return_value.write_tag.call_count, 0)
        blk.stop()

    @patch(WriteTag.__module__ + '.ClxDriver')
    def test_signal_lists(self, mock_clx):
        """Outgoing signal lists are the same length as input"""
        blk = WriteTag()
        self.configure_block(blk, {'host': 'ip_addr', 
                                   'tags': ('pi', 3.14, 'irrational')})
        blk.start()
        blk.process_signals([Signal(), Signal()])
        blk.stop()
        self.assertEqual(2, len(self.notified_signals[DEFAULT_TERMINAL][-1]))

    @patch(WriteTag.__module__ + '.ClxDriver')
    def test_signal_enrichment(self, mock_clx):
        """Block mixin is implemented correctly"""
        mock_read_values = (1, 'INT')
        mock_clx.return_value.write_tag.return_value = True
        blk = WriteTag()
        self.configure_block(blk, {'host': 'ip_addr',
                                   'tags': ('pi', 3.14, 'irrational'),
                                   'enrich': {'exclude_existing': False}})
        blk.start()
        blk.process_signals([Signal({'pi': 3.14})])
        blk.stop()
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'success': True, 'pi': 3.14})

