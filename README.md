# Block Template

The Block Template is a base template used to create a new block type with the recommended files and file structure.

//Summary sentence should contain a concise description of the block//

## How to Use

//This should stand independently of the docs and we should not link back and forth--besides, the link doesn't show how to make a new directory without cloning. Instead, link to the readme file for the project template. //

Before cloning the block template, create your first project.... //Would this work just to show the prerequisite / starting point?//

To create a project directory, follow the instructions here: [First Project](https://docs.n.io/getting_started/locally.html#first-project).


### Clone the Block Template -- 
//These instructions are not the same as in our docs. Check with Chris/Andrew/Ben or someone to determine the preferred method.//

  1. From the command line, navigate to the `/blocks` folder.
      
      `cd nio/projects/<project_name>/blocks`
  2. Clone the block template. Use a meaningful name to describe the block's function.
      
      `git clone --depth=1 https://github.com/nio-blocks/block_template.git <new_block_name>`
  2. Navigate to the new block folder.
      
      `cd <new_block_name>`

### Rename the Appropriate Files

  1. Rename `example_block.py` to the name of your new block. Note: The filename which should end in `_block.py`. 
    
        `mv example_block.py new_name_block.py`
  1. Edit this file and rename `class Example(Block)` to `class New_Name(Block)`. Note: You do not need to include `Block` in the class name since this is implied in the block name. 
  
  1. Rename `BLOCK_README.md` to `README.md` and update the contents of this file

        `mv BLOCK_README.md README.md`
  1. In the `/tests` folder, rename `test_example_block.py` to match the class name of your new block
      
        `mv test_example_block.py new_name_block.py`

### Track Your New Block on GitHub

  1. Create a new GitHub repository. For convenience, use the same name as `<new_block_name>`, and then copy the URL. //Why are you copying the URL? Where is this used?//
  1. Remove the tracking link to the original template repository

       `git remote remove origin`
  1. Stage the new files

        `git add -A`
  1. Reset ownership to yourself

        `git commit --amend --reset-author -m "Initial Commit"`
  1. Add tracking to the new remote repository using the URL you copied //is this correct?//

        `git remote add origin <new_repo_url>`
  1. Push to a branch (usually `master`)

        `git push --set-upstream origin master`

### File Reference

**example_block.py**<br>This is the block code. Additional Python classes and files are definitely welcome. If the file contains a block class, make sure the filename ends with `_block.py`. If the file represents a base block that is not discoverable by itself, rename the filename to end with `_base.py`. //Is it just good practice to rename a base block--whether it is discoverable or not--with _base.py?//

**requirements.txt**
<br>Lists required Python dependencies. The file is installed by pip when the block is installed. To install the dependencies, enter `pip install -r requirements.txt`.

**spec.json**<br>
Defines the block specifications. The metadata is used for block discovery.

**release.json**<br>Contains release data for one or more blocks.

**tests/test_example_block.py**<br>Always submit accompanying unit tests in the `tests` folder. //Does not define what is in the file//
