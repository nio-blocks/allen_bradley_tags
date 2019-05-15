allen_bradley_tags
===

Blocks in this Collection
---
[CLXReadTag](docs/clx_read_tag_block.md)  
[CLXWriteTag](docs/clx_write_tag_block.md)

Dependencies
---
[pycomm3](https://github.com/bpaterni/pycomm/tree/pycomm3)

When installing `requirements.txt`, pip will attempt to install the pycomm3 fork and if a conflict is found it will prompt for resolution. If the wrong fork is installed, the block will fail to configure raising `pycomm.cip.cip_base.CommError: must be str, not bytes`.
