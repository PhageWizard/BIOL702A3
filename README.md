# Generate a Phylogenetic tree

This script generates a phylogenetic tree by utilizing muscle
to conduct multi-sequence alignment, and mrbayes to generate the tree.

## Setup

This script is designed for Unix-like systems (e.g., macOS or Linux). 
You will need to install developer tools, which you can set up by running 
Python in the terminal to trigger the installation prompt. 
Additionally, Homebrew is required and can be installed by following the instructions at
https://docs.brew.sh/Installation.

Ensure the following steps are conducted in a terminal:

1. Create a new Python virtual environment and activate it:
```zsh
# This needs to be done once to create the venv.
python3 -m venv env

# Before using the venv you need to activate it.
source env/bin/activate
```
2. Install the dependencies from the requirements.txt file:
```zsh
pip install -r requirements.txt
```

3. Install MUSCLE and MrBayes via Brew:
```zsh
brew tap brewsci/bio
brew install muscle
brew install mrbayes
```

5. Run the script with the desired concatenated FASTA sequences (filamentous_phages.fas).
```zsh
python generate_tree.py --file filamentous_phages.fas
```

This will now perform a multi-sequence alignment, then tree construction which
will take a couple of minutes.

The result should be a file named `last_tree.png` which will contain the phylogenetic
tree built from the provided sequences.






