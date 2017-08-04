# Block Template

The Block Template is a base template used to create a new block type with the recommended files and file structure.

## How to Use

If you need to first create a project directory, the [`project_template` (https://github.com/nioinnovation/project_template](https://github.com/nioinnovation/project_template) repository provides a good starting point.

### Clone the Block Template

  1. From the command line, navigate to the `/blocks` folder in your project.

      `cd nio/projects/<project_name>/blocks`
  2. Clone the block template. Use a meaningful name to describe the block's function.

      `git clone --depth=1 https://github.com/nio-blocks/block_template.git <new_block_name>`
  2. Navigate to the new block folder.

      `cd <new_block_name>`

### Rename the Appropriate Files

  1. Rename `example_block.py` to the name of your new block. Note: The filename should end in `_block.py` or `_base.py`. Use `_block.py` if it is intended to be a discoverable block and `_base.py` if it is meant to have common, reusable base functionality but not be discoverable.

        `mv example_block.py new_name_block.py`
  1. Edit this file and rename `class Example(Block)` to `class New_Name(Block)`. Note: You do not need to include `Block` in the class name since this is implied in the block name.

  1. Rename `BLOCK_README.md` to `README.md` and update the contents of this file.

        `mv BLOCK_README.md README.md`
  1. In the `/tests` folder, rename `test_example_block.py` to match the class name of your new block.

        `mv test_example_block.py new_name_block.py`
  1. Edit this file and rename `class TestExample(NIOBlockTestCase)` to `class TestNew_Name(NIOBlockTestCase)`.

### Track Your New Block on GitHub

  1. Create a new GitHub repository. For convenience, use the same name as `<new_block_name>`, and then copy the **Clone or download** URL.

  1. Remove the tracking link to the original template repository.

       `git remote remove origin`
  1. Stage the new files.

        `git add -A`
  1. Reset ownership to yourself.

        `git commit --amend --reset-author -m "Initial Commit"`
  1. Add tracking to the new remote repository using the URL you copied.

        `git remote add origin <new_repo_url>`
  1. Push to a branch (usually `master`).

        `git push --set-upstream origin master`

### File Reference

**example_block.py**<br>This is the block code. Additional Python classes and files are definitely welcome. If the file contains a block class, make sure the filename ends with `_block.py`. If the file represents a base block (a block type that is not intended to be discoverable by itself), rename the filename to end with `_base.py`.

**requirements.txt**
<br>Lists required Python dependencies. The file is installed by pip when the block is installed. To install the dependencies, enter `pip install -r requirements.txt`.

**spec.json**<br>
Defines the block specifications. The metadata is used for block discovery.

**release.json**<br>Contains release data for one or more blocks.

***spec.json**<br>Defines the specification for a block type. This is the metadata which is used for block discovery.

**tests/test_example_block.py**<br>The `tests` folder contains a sample test file. Be sure to submit accompanying unit tests with your blocks.
