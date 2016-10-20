####This is a simple python3 script to extract particular sets of aligned residues
from a fasta formatted alignment file####

There are **2** arguments:
    
    1. alignment:  Fasta formatted alignment file

    2. residues:   Space separated list of zero-indexed residue indices to
                   extract. For example, a 0 will extract the first residue.
                   This position is relative to the main sequence, which 
                   is assumed to be the first sequence in the fasta file, 
                   but can be changed (SEE BELOW)

The script will indicate the sequence that is being used as main and ask if
a different sequence should be used. If the option to choose a different 
sequence is selected, then a list of sequence options is provided for selection

The script will ask several questions about sequence output regarding:
- Sequence names being included
- Main sequence being included
- Output to screen or file
