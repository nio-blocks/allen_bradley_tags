# Block Template

This repository serves as a "starter" repository for creating a new block.

## How to Use

### Clone the Block Template

1. Using the command line, navigate into your project's `/blocks` folder: `cd nio/projects/<project_name>/blocks` (If you need to create a project directory, follow the instructions here: [First Project](https://docs.n.io/getting_started/locally.html#first-project)).

2. Clone the block template: `git clone --depth=1 https://github.com/nio-blocks/block_template.git <new_block_name>`

2. Navigate into the new block folder: `cd <new_block_name>`

### Rename the Appropriate Files

1. Rename `example_block.py` to the name of your new block.
1. In your new block Python file, rename the `Example` class to the new block's name. Avoid putting `Block` in the class name, this is implied of the filename which should end in `_block.py`
1. Rename `test_example_block.py` to match your new block's class name.
1. Rename `BLOCK_README.md` to `README.md`: `mv BLOCK_README.md README.md` and update the contents with your new documentation.

### Track Your New Block on GitHub

1. Create a new GitHub repository, often this will have the same name as `<new_block_name>`, and copy the URL
1. Remove the tracking link to the original template repository: `git remote remove origin`
1. Stage your new files: `git add -A`
1. Take ownership: `git commit --amend --reset-author -m "Initial Commit"`
1. Add tracking to your new remote repository: `git remote add origin <new_repo_url>`
1. Push your work to a branch (usually `master`): `git push --set-upstream origin master`

### File Reference

 * **example_block.py** : This is the block code. Additional Python classes and files are definitely welcome. If the file contains a Block class, make sure the filename ends with `_block.py`. If the file represents a Base Block that is not discoverable by itself, have the filename end with `_base.py`.
 * **requirements.txt** : List out any Python dependencies this block requires. This file will be installed by pip when the block is installed. The command for installing the dependencies is `pip install -r requirements.txt`.
 * **spec.json** : Define the specification for a block, this is the metadata which is used for block discovery.
 * **release.json** : The release data for one or more blocks.
 * **tests/test_example_block.py** : Always submit accompanying unit tests in the `tests` folder.
