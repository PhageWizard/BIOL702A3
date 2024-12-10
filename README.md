# Generate a Phylogenetic tree

This script generates a phylogenetic tree through the orchastration of muscle,
to conduct multi-sequence alignment and mrbayes to generate the tree.

## Setup

This expects the user to be on a unix like system (i.e. MacOS or Linux). You
will need to have developer tools installed (which you can do by running
`python` in the terminal which will bring up a prompt to install them). You
will also need brew, which you can install from
https://docs.brew.sh/Installation.

Ensure the following is conducted in a terminal!

1. Create a new python virtual environment and activate it:
```zsh
# This just needs to be done once to create the venv.
python3 -m venv env

# Prior to using the venv you need to run this.
source env/bin/activate
```
2. Install the dependencies from the requirements.txt file:
```zsh
pip install -r requirements.txt
```

3. Install MUSCLE and MrBayes via brew:
```zsh
brew tap brewsci/bio
brew install muscle
brew install mrbayes
```

5. Run the script with the desired concatenated FASTA sequences (i.e. filamentous_phages.fas).
```zsh
python generate_tree.py --file filamentous_phages.fas
```

This will now perform a multi-sequence alignment, then tree construction which
will take around 30 - 40 minutes(atleast for my MacBook Air).

The result should be a file: `last_tree.png` which will depict the phylogeny
tree for the provided sequences.






