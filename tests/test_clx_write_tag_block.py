from unittest.mock import patch, Mock
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..clx_write_tag_block import CLXWriteTag


class CustomException(Exception):

    pass


class TestCLXWriteTag(NIOBlockTestCase):

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_write_tag(self, mock_clx):
        """A valid tag is written and successful status notified"""
        tag_to_write = ('seven', 7, 'INT')
        tag_expr = '{{ (\'seven\', 7, \'INT\') }}'
        # write_tag returns a bool indicating success
        drvr = mock_clx.return_value
        drvr.write_tag.return_value = True
        config = config = {
            'host': 'ip_addr',
            'tags': tag_expr,
        }
        blk = CLXWriteTag()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        drvr.write_tag.assert_called_once_with(tag_to_write)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'host': 'ip_addr', 'success': True})

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_write_multiple_tags(self, mock_clx):
        """Multiple tags are written with varied success"""
        tags_to_write = [('seven', 7, 'INT'), ('pi', 3.14, 'REAL')]
        tag_expr = '{{ [(\'seven\', 7, \'INT\'), (\'pi\', 3.14, \'REAL\')] }}'
        # write_tag returns a list of tuples (name, value, type, "GOOD"|"BAD")
        drvr = mock_clx.return_value
        drvr.write_tag.return_value = [
            ('seven', 7, 'INT', 'GOOD'),  ('pi', 3.14, 'REAL', 'BAD')]
        config = {
            'host': 'ip_addr',
            'tags': tag_expr,
        }
        blk = CLXWriteTag()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        drvr.write_tag.assert_called_once_with(tags_to_write)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'host': 'ip_addr', 'success': [True, False]})

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_write_invalid_tag(self, mock_clx):
        """Only write tags that are inside a valid tuple"""
        drvr = mock_clx.return_value
        config = {
            'host': 'ip_addr',
            'tags': 'not a tuple',
        }
        blk = CLXWriteTag()
        self.configure_block(blk, config)
        blk.start()
        with self.assertRaises(TypeError):
            blk.process_signals([Signal()])
        self.assertEqual(drvr.write_tag.call_count, 0)
        blk.stop()

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_write_tags_one_invalid(self, mock_clx):
        """No tags are written if any of them are not a valid tuple"""
        tag_expr = '{{ [(\'seven\', 7, \'INT\'), \'not a tuple\'] }}'
        drvr = mock_clx.return_value
        config = {
            'host': 'ip_addr',
            'tags': tag_expr,
        }
        blk = CLXWriteTag()
        self.configure_block(blk, config)
        blk.start()
        with self.assertRaises(TypeError):
            blk.process_signals([Signal()])
        # if any tag in a list is invalid, no write_tag call is made
        self.assertEqual(drvr.write_tag.call_count, 0)
        blk.stop()

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_signal_lists(self, mock_clx):
        """Outgoing signal lists are the same length as input"""
        config = {
            'host': 'ip_addr',
            'tags': ('pi', 3.14, 'irrational'),
        }
        blk = CLXWriteTag()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal(), Signal()])
        blk.stop()
        self.assertEqual(2, len(self.notified_signals[DEFAULT_TERMINAL][-1]))

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_signal_enrichment(self, mock_clx):
        """Block mixin is implemented correctly"""
        mock_read_values = (1, 'INT')
        drvr = mock_clx.return_value
        drvr.write_tag.return_value = True
        config = {
            'host': 'ip_addr',
            'tags': ('pi', 3.14, 'irrational'),
            'enrich': {
                'exclude_existing': False,
            },
        }
        blk = CLXWriteTag()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal({'pi': 3.14})])
        blk.stop()
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'host': 'ip_addr', 'success': True, 'pi': 3.14})

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_connection_fails(self, mock_clx):
        """The block can start even if the initial connection fails."""
        drvr = mock_clx.return_value
        drvr.open.side_effect = CustomException
        blk = CLXWriteTag()
        config = {
            'host': 'ip_addr',
            'tags': ('pi', 3.14, 'irrational'),
        }
        self.configure_block(blk, config)
        self.assertEqual(drvr.open.call_count, 1)
        self.assertEqual(drvr.open.call_args[0], ('ip_addr', ))
        self.assertIsNone(blk.cnxn)
        # start processing signals and try (and fail) to reopen connection
        blk.start()
        blk.process_signals([Signal()])
        self.assertEqual(drvr.open.call_count, 2)
        # still no connection
        drvr.write_tag.assert_not_called()
        self.assertIsNone(blk.cnxn)
        blk.stop()
        # no connection so nothing to close
        drvr.close.assert_not_called()
        self.assert_num_signals_notified(0)

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_reconnection(self, mock_clx):
        """Processing signals reopens the connection."""
        drvr = mock_clx.return_value
        drvr.open.side_effect = [CustomException, Mock()]
        blk = CLXWriteTag()
        config = {
            'host': 'ip_addr',
            'tags': ('pi', 3.14, 'irrational'),
        }
        self.configure_block(blk, config)
        self.assertEqual(drvr.open.call_count, 1)
        self.assertEqual(drvr.open.call_args[0], ('ip_addr', ))
        self.assertIsNone(blk.cnxn)
        # start processing signals and reopen connection
        blk.start()
        blk.process_signals([Signal()])
        self.assertEqual(drvr.open.call_count, 2)
        self.assertEqual(blk.cnxn, drvr)
        self.assertEqual(drvr.write_tag.call_count, 1)
        blk.stop()
        self.assertEqual(drvr.close.call_count, 1)
        self.assertIsNone(blk.cnxn)
        self.assert_num_signals_notified(1)

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_reconnection_fails(self, mock_clx):
        """When out of retries, reset the connection."""
        drvr = mock_clx.return_value
        drvr.write_tag.side_effect = CustomException
        blk = CLXWriteTag()
        config = {
            'host': 'ip_addr',
            'tags': ('pi', 3.14, 'irrational'),
            'retry_options': {
                'max_retry': 0,  # do not retry
            },
        }
        self.configure_block(blk, config)
        blk.start()
        self.assertEqual(blk.cnxn, drvr)
        blk.process_signals([Signal()])
        self.assertIsNone(blk.cnxn)
        blk.stop()

    @patch(CLXWriteTag.__module__ + '.ClxDriver')
    def test_retry_connection_before_retry_request(self, mock_clx):
        """When a request fails, the connection is retried first."""
        drvr = mock_clx.return_value
        drvr.write_tag.side_effect = [CustomException, CustomException, True]
        blk = CLXWriteTag()
        config = {
            'host': 'ip_addr',
            'tags': ('pi', 3.14, 'irrational'),
            'retry_options': {
                'max_retry': 2,  # make three total attempts
                'multiplier': 0, # don't wait while testing
            },
        }
        self.configure_block(blk, config)
        self.assertEqual(drvr.open.call_count, 1)
        self.assertEqual(blk.cnxn, drvr)
        blk.start()
        blk.process_signals([Signal()])
        self.assertEqual(drvr.write_tag.call_count, 3)
        # Before each retry to read_tag() the connection is
        # retried and read_tag works on the third attempt
        self.assertEqual(drvr.close.call_count, 2)
        self.assertEqual(drvr.open.call_count, 3)
        blk.stop()
        self.assertEqual(drvr.close.call_count, 3)
        self.assert_last_signal_notified(Signal({
            'host': 'ip_addr',
            'success': True,
        }))
