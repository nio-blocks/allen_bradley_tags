ReadTag
=======
Read tags from an Allen-Bradley ControlLogix or CompactLogix PLC.

Properties
----------
- **enrich**: Signal Enrichment
  - *exclude_existing*: If checked (true), the attributes of the incoming signal will be excluded from the outgoing signal. If unchecked (false), the attributes of the incoming signal will be included in the outgoing signal.
  - *enrich_field*: (hidden) The attribute on the signal to store the results from this block. If this is empty, the results will be merged onto the incoming signal. This is the default operation. Having this field allows a block to 'save' the results of an operation to a single field on an incoming signal and notify the enriched signal.
- **host**: IP address or hostname of target device.
- **tags**: A tag (string), or list of tags, to read.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A list of signals of equal length to input.
  * *value* (tuple): The requested value and data type as `(name, value, type)`, or a list of tuples if more than one tag was read.

Commands
--------
None

Dependencies
------------
[pycomm3](https://github.com/bpaterni/pycomm/tree/pycomm3)  
When installing `requirements.txt`, pip will attempt to install the pycomm3 fork and if a conflict is found it will prompt for resolution. If the wrong fork is installed, the block will fail to configure raising `pycomm.cip.cip_base.CommError: must be str, not bytes`.



***

WriteTag
========
Write tags to an Allen-Bradley ControlLogix or CompactLogix PLC.

Properties
----------
- **enrich**: Signal Enrichment
  - *exclude_existing*: If checked (true), the attributes of the incoming signal will be excluded from the outgoing signal. If unchecked (false), the attributes of the incoming signal will be included in the outgoing signal.
  - *enrich_field*: (hidden) The attribute on the signal to store the results from this block. If this is empty, the results will be merged onto the incoming signal. This is the default operation. Having this field allows a block to 'save' the results of an operation to a single field on an incoming signal and notify the enriched signal.
- **host**: IP address or hostname of target device.
- **tags**: A tuple, or list of tuples, of `(name, value, type)` to write.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: A list of signals of equal length to input.
  * *success* (bool): `True` if the write operation was successful, otherwise `False`, or a list of booleans if more than one tag was written.

Commands
--------
None

Dependencies
------------
[pycomm3](https://github.com/bpaterni/pycomm/tree/pycomm3)  
When installing `requirements.txt`, pip will attempt to install the pycomm3 fork and if a conflict is found it will prompt for resolution. If the wrong fork is installed, the block will fail to configure raising `pycomm.cip.cip_base.CommError: must be str, not bytes`.

