# Block Template

This repository serves as a "starter" repository for creating a new block.

## How to use

### Get the Block Template

1. Using the command line, navigate to your nio project's blocks folder: `cd nio/projects/<project_name>/blocks`
1. `git clone https://github.com/nio-blocks/block_template.git <new_block_name>`
1. Navigate into the new block folder: `cd <new_block_name>`

### Rename the Appropriate Files

1. Rename `example_block.py` to whatever your block name will be.
1. In your new block Python file, rename the `Example` class to the new block's name.
1. Rename `test_example_block.py` to match your new block's class name.
1. Rename `BLOCK_README.md` to `README.md` and update the documentation accordingly.

### Track Your New Block on GitHub

1. Create a new GitHub repository, often this will have the same name as `<new_block_name>`, and copy the URL
1. Your new block will no longer track the template: `git remote remove origin`
1. Stage your new files: `git add -A`
1. Take ownership: `git commit --amend --reset-author -m "Inital Commit"`
1. Set up your block to track your remote repository: `git remote add origin <new_repo_url>`
1. Push your work to a branch (usually `master`): `git push --set-upstream origin master`

## File Reference

 * **example_block.py** : This is the block code. Additional Python classes and files are definitely welcome. If the file contains a Block class, make sure the filename ends with `_block.py`. If the file represents a Base Block that is not discoverable by itself, have the filename end with `_base.py`.
 * **requirements.txt** : List out any Python dependencies this block requires. This file will be installed by pip when the block is installed. The command for installing the dependencies is `pip install -r requirements.txt`.
 * **spec.json** : Define the specification for a block, this is the metadata which is used for block discovery.
 * **release.json** : The release data for one or more blocks.
 * **tests/test_example_block.py** : Always submit accompanying unit tests in the `tests` folder.
 * **requirements.txt** : List out any Python dependencies this block requires. This file will be installed by pip when the block is installed. The command for installing the dependencies is `pip install -r requirements.txt`.