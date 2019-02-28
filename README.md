allen_bradley_tags
===

Blocks in this Collection
---
[ReadTag](docs/read_tag_block.md)
[WriteTag](docs/write_tag_block.md)

Dependencies
---
[pycomm3](https://github.com/bpaterni/pycomm/tree/pycomm3)

When installing `requirements.txt`, pip will attempt to install the pycomm3 fork and if a conflict is found it will prompt for resolution. If the wrong fork is installed, the block will fail to configure raising `pycomm.cip.cip_base.CommError: must be str, not bytes`.