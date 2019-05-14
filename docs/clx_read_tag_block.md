CLXReadTag
=======
Read tags from an Allen-Bradley ControlLogix or CompactLogix PLC.

Properties
----------
- **Host Address**: IP address or hostname of target device.
- **Tags**: A tag (string), or list of tags, to read.

Example
-------
For every request processed, the output signal will contain the following attributes, plus any **Signal Enrichement** options. If the request was not successful the signal will be dropped.
  - *host* (string) The hostname of the target device.
  - *value* (tuple): The requested value and data type as `(name, value, type)`, or a list of tuples if more than one tag was read.

Commands
--------
None
