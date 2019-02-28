from unittest.mock import patch, Mock
from nio.block.terminals import DEFAULT_TERMINAL
from nio.signal.base import Signal
from nio.testing.block_test_case import NIOBlockTestCase
from ..read_tag_block import ReadTag


class CustomException(Exception):

    pass


class TestReadTag(NIOBlockTestCase):

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_read_tag(self, mock_clx):
        """A tag is read is its value notified"""
        # if passes only a string, read_tag returns (value, type)
        tag = 'foo'
        mock_read_values = (3.14, 'REAL')
        mock_clx.return_value.read_tag.return_value = mock_read_values
        config = {
            'host': 'ip_addr',
            'tags': '{{ $tag }}',
        }
        blk = ReadTag()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal({'tag': tag})])
        blk.stop()
        mock_clx.return_value.open.assert_called_once_with('ip_addr')
        mock_clx.return_value.close.assert_called_once_with()
        mock_clx.return_value.read_tag.assert_called_once_with(tag)
        self.assert_num_signals_notified(1)
        # we add the tag name to the returned value
        expected_value = (tag, ) + mock_read_values
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'host': 'ip_addr', 'value': expected_value})

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_read_multiple_tags(self, mock_clx):
        """A list of tags is read, notifying a list of values"""
        # read_tag returns a list of tuples of (name, value, type)
        tags = ['foo', 'bar', 'baz']
        tag_expr = '{{' + '[\'{}\', \'{}\', \'{}\']'.format(*tags) + '}}'
        mock_read_values = [
            (tags[0], 0, 'INT'), (tags[1], 1, 'DINT'), (tags[2], 2.0, 'REAL')]
        mock_clx.return_value.read_tag.return_value = mock_read_values
        config = {
            'host': 'ip_addr',
            'tags': tag_expr,
        }
        blk = ReadTag()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal()])
        blk.stop()
        mock_clx.return_value.read_tag.assert_called_once_with(tags)
        self.assert_num_signals_notified(1)
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'host': 'ip_addr', 'value': mock_read_values})

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_signal_lists(self, mock_clx):
        """Outgoing signal lists are the same length as input"""
        config = {
            'host': 'ip_addr',
            'tags': 'foo',
        }
        blk = ReadTag()
        self.configure_block(blk, config)
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
        config = {
            'host': 'ip_addr',
            'tags': tag,
            'enrich': {
                'exclude_existing': False,
            },
        }
        blk = ReadTag()
        self.configure_block(blk, config)
        blk.start()
        blk.process_signals([Signal({'pi': 3.14})])
        blk.stop()
        expected_value = (tag,) + mock_read_values
        self.assertDictEqual(
            self.last_notified[DEFAULT_TERMINAL][0].to_dict(),
            {'host': 'ip_addr', 'pi': 3.14, 'value': expected_value})

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_connection_fails(self, mock_clx):
        """The block can start even if the initial connection fails."""
        drvr = mock_clx.return_value
        drvr.open.side_effect = CustomException
        blk = ReadTag()
        config = {
            'host': 'ip_addr',
            'tags': 'foo',
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
        drvr.read_tag.assert_not_called()
        self.assertIsNone(blk.cnxn)
        blk.stop()
        # no connection so nothing to close
        drvr.close.assert_not_called()
        self.assert_num_signals_notified(0)

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_reconnection(self, mock_clx):
        """Processing signals reopens the connection."""
        drvr = mock_clx.return_value
        drvr.open.side_effect = [CustomException, Mock()]
        blk = ReadTag()
        config = {
            'host': 'ip_addr',
            'tags': 'foo',
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
        self.assertEqual(drvr.read_tag.call_count, 1)
        blk.stop()
        self.assertEqual(drvr.close.call_count, 1)
        self.assertIsNone(blk.cnxn)
        self.assert_num_signals_notified(1)

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_reconnection_fails(self, mock_clx):
        """When out of retries, reset the connection."""
        drvr = mock_clx.return_value
        drvr.read_tag.side_effect = CustomException
        blk = ReadTag()
        config = {
            'host': 'ip_addr',
            'tags': 'foo',
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

    @patch(ReadTag.__module__ + '.ClxDriver')
    def test_retry_connection_before_retry_request(self, mock_clx):
        """When a request fails, the connection is retried first."""
        mock_read_values = (3.14, 'REAL')
        drvr = mock_clx.return_value
        drvr.read_tag.side_effect = [
            CustomException, CustomException, mock_read_values]
        blk = ReadTag()
        config = {
            'host': 'ip_addr',
            'tags': 'foo',
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
        self.assertEqual(drvr.read_tag.call_count, 3)
        # Before each retry to read_tag() the connection is 
        # retried and read_tag works on the third attempt
        self.assertEqual(drvr.close.call_count, 2)
        self.assertEqual(drvr.open.call_count, 3)
        blk.stop()
        self.assertEqual(drvr.close.call_count, 3)
        self.assert_last_signal_notified(Signal(
            {'host': 'ip_addr', 'value': ('foo', 3.14, 'REAL')}))
