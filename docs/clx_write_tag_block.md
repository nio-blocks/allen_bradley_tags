CLXWriteTag
========
Write tags to an Allen-Bradley ControlLogix or CompactLogix PLC.

Properties
----------
- **Host Address**: IP address or hostname of target device.
- **Tags**: A tuple, or list of tuples, of `(name, value, type)` to write.

Example
-------
  - *host* (string) The hostname of the target device.
  - *success* (bool): `True` if the write operation was successful, otherwise `False`, or a list of booleans if more than one tag was written.

Commands
--------
None
