# Block Template

This repository serves as a "starter" repository for creating a new block.

## How to use

### Get the block template

 1. Clone this repository: `git clone https://github.com/nio-blocks/block_template.git --depth=1 --single-branch -b <branch_name> <new_block_name>`
  - `<branch_name>` is either "master" or "nio2" depending on the target version for nio 
 2. Go into the directory: `cd <new_block_name>`
 3. Remove to template origin: `git remote remove origin`
 4. Take ownership of the initial commit: `git commit --amend --reset-author -m 'Initial Commit'`
 3. Add new block repo as remote: `git remote add origin [new_block_repo]`
 4. Push: `git push --set-upstream origin <remote_branch_name>:<local_branch_name>`


### Rename the appropriate files

 1. Rename `example_block.py` to whatever your block name will be. We like to keep `_block` at the end of filenames that contain blocks.
 1. In your new block Python file, rename the class to the new block's name. Do **not** put `Block` in the class name - this is implied.
 1. Rename `test_example_block.py` to match your new block's class name. Always submit accompanying unit tests in the `tests` folder.
 1. Rename `BLOCK_README.md` to `README.md` and update the documentation accordingly.


## File Reference

 * **example_block.py** : This is the block code. Additional Python classes and files are definitely welcome. If the file contains a Block class, make sure the filename ends with `_block.py`. If the file represents a Base Block that is not discoverable by itself, have the filename end with `_base.py`.
 * **requirements.txt** : List out any Python dependencies this block requires. This file will be installed by pip when the block is installed. The command for installing the dependencies is `pip install -r requirements.txt`.
