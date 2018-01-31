# Block template

The block template is a base template used to create a new block type with the recommended files and file structure.

---

## How to use

The nio-cli `newblock` command creates a custom block from this repository. This command clones the project, renames all of the example files, and sets the initial commit for your new block.

Run this command from the `blocks/` directory of your nio project.

```bash
nio newblock <new_block>
```

If you need to first create a nio project, use the nio-cli `nio-new` command

```bash
nio new <new_project>
```

For more information about your project directory, refer to the `project_template` repository at <https://github.com/niolabs/project_template> 


---

## File reference

**<new_block>_block.py**<br>This is the block code. Additional Python classes and files are definitely welcome. If the file contains a block class, make sure the filename ends with `_block.py`. If the file represents a base block (a block type that is not intended to be discoverable by itself), rename the filename to end with `_base.py`.

**requirements.txt**<br>Lists required Python dependencies. The file is installed by pip when the block is installed. To install the dependencies, enter `pip install -r requirements.txt`.

**release.json**<br>Contains release data for one or more blocks.

**spec.json**<br>Defines the specification for a block type. This is the metadata which is used for block discovery.

**tests/test_<new_block>_block.py**<br>The **tests** folder contains a sample test file. Be sure to submit accompanying unit tests with your blocks.
