import subprocess as sp
import os
from argparse import ArgumentParser

import matplotlib.pyplot as plt
from Bio import Phylo
from Bio import AlignIO

# This script assumes the user is using MacOS or atleast a Unix like system.
# Setup:
#  - install muscle https://www.drive5.com/muscle/manual/install.html - used for multi-sequence alignment
#  - install MrBayes https://github.com/NBISweden/MrBayes/blob/develop/INSTALL - used for tree construction
#  - create a local python virtual environment and install biopython

# N.B. MyBayes only supports ascii and will crash if it encounters unicode (like Phi)


def alignSequences(concatenated_fasta_path, aligned_sequences_path):
    args = [
        "muscle",
        "-align",
        concatenated_fasta_path,
        "-output",
        aligned_sequences_path,
        "-threads",
        "2",
    ]
    if sp.run(args).returncode != 0:
        raise SystemError(
            "Failed to run Muscle, please ensure it is installed and visible within your PATH."
        )


def fromAfaToNex(aligned_sequences_path, nex_path):
    align = list(AlignIO.parse(aligned_sequences_path, "fasta"))
    if not align:
        raise ArgumentError(
            f"Provided aligned sequences: {aligned_sequences_path} is empty!"
        )
    # We need to explicitly assign the molecule_type as AlignIO.parse is unable to determine this.
    for seq in align[0]:
        seq.annotations["molecule_type"] = "DNA"
    with open(nex_path, "w") as f:
        AlignIO.write(align, f, "nexus")


def removeNonAscii(file_path):
    """Preserves only ascii characters in file, required by MrBayes."""
    data = None
    with open(file_path, "r") as f:
        data = f.read()
    if not data:
        raise ArgumentError(f"Failed to read: {file_path} or is empty.")
    with open(file_path, "w") as f:
        f.write(data.encode("ascii", errors="ignore").decode())


def injectMrBayesDirectives(
    nex_path, ngen=200000, samplefreq=500, printfreq=500, diagnfreq=5000
):
    """MrBayes requires directives to be added to the nex file.

    Add the directives for a typical run of mcmc based tree construction.
    """

    BAYES_DIRECTIVES = f"""
      begin mrbayes;
          set autoclose=yes nowarn=yes;
          lset nst=6 rates=invgamma;
          mcmc ngen={ngen} samplefreq={samplefreq} printfreq={printfreq} diagnfreq={diagnfreq};
          sump;
          sumt;
      end;
      """
    with open(nex_path, "a") as f:
        f.write(BAYES_DIRECTIVES)


def invokeMrBayes(nex_path):
    if sp.run(["mb", nex_path]).returncode != 0:
        raise SystemError(
            "Failed to run MyBayes, please ensure it is installed and visible "
            "within your PATH."
        )


def app(args):
    AFA_PATH = "aligned.afa"
    NEX_PATH = "aligned.nex"

    alignSequences(args.file, AFA_PATH)
    fromAfaToNex(AFA_PATH, NEX_PATH)
    removeNonAscii(NEX_PATH)
    injectMrBayesDirectives(NEX_PATH, ngen=args.mr_bayes_ngen)
    invokeMrBayes(NEX_PATH)

    # Plot the final tree from the MCMC search.
    last_tree = list(Phylo.parse(".".join([NEX_PATH, "run2", "t"]), "nexus"))[-1]
    fig, ax = plt.subplots(1, 1, figsize=(12,8))
    Phylo.draw(last_tree, axes=ax, branch_labels=lambda c:f"{c.branch_length:.2f}" if c.branch_length > 0.01 else "", do_show=False)
    plt.savefig("last_tree.png")
    print("Phylo Tree saved to ./last_tree.png")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--file",
        help="Concatenated fasta sequences for targeted collection of species "
        "of interest.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "--mr_bayes_ngen",
        help="Value passed to MrBayes ngen, corresponding to the number of "
        "generations to be run, in the interest of saving the user time this "
        "is set to the small value of 20000, for a full run consider setting "
        "this to 1000000",
        default=20000,
    )
    args = parser.parse_args()
    app(args)
