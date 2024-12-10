# Generate a Phylogenetic tree

This script generates a phylogenetic tree through the orchastration of muscle,
to conduct multi-sequence alignment and mrbayes to generate the tree.

## Setup
This expects the user to be on a unix like system (i.e. MacOS or Linux).

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

3. Download MUSCLE from https://github.com/rcedgar/muscle/releases for your OS and add it to your PATH:
```zsh
# Download using curl (standard on MacOS terminal).
curl -L https://github.com/rcedgar/muscle/releases/download/v5.3/muscle-osx-arm64.v5.3 --output muscle

# Make muscle executable.
chmod +x muscle

# Add muscle to your PATH. This will only persist as long as the shell is open, so you need to run again later in a new shell.
export PATH=$PATH:$( realpath muscle )
```

4. Following the Install instructions for MrBayes from https://github.com/NBISweden/MrBayes/blob/develop/INSTALL

5. Run the script with the desired concatenated FASTA sequences (i.e. filamentous_phages.txt).
```zsh
python generate_tree.py --file filamentous_phages.txt
```
This will now perform a multi-sequence alignment, then tree construction which will take around 30 - 40 minutes(atleast for my MacBook Air).

The result should be a file: `last_tree.png` which will depict the phylogeny tree for the provided sequences.






