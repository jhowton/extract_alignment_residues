#!/usr/bin/python3

import sys

# Ensure all args present
if len(sys.argv) != 3:
    print("\nPlease supply alignment file and a list of residue indices:")
    print("\t{} alignment residues".format(sys.argv[0]))
    print("\t\talignment: Alignment file in fasta format")
    print("\t\tresidues: File with space-separated, zero-indexed")
    print("\t\t\tresidues of interest for top sequence in alignment\n")
    exit()

# Read in indices of residues of interest
with open(sys.argv[2]) as res_file:
    res_ind = sorted([int(ind) for ind in res_file.readline().strip().split(' ')])

seqs = {} # Dictionary of sequences
curr = "" # Current Sequence string

# Read in sequences to dictionary (seqs) 
with open(sys.argv[1]) as fasta:
    for line in fasta:

        # Check if line is name of seq
        if line[0] == '>':
            # Check if first sequence
            if curr=="":
                # Store name of first sequence
                main_seq = line.strip()
                curr = main_seq
            else:
                curr = line.strip()
            seqs[curr] = ""

        # Add sequence portion to dictionary (seqs)
        elif curr != "":
            seqs[curr] += line.strip()

# Ask if current main is main sequence
print("The sequence \'{}\' is currently being used as the main sequence".format(main_seq[1:]))
while True:
    keep_main_val = input("Is this the correct main sequence? Y/n   ").lower()
    if keep_main_val == 'y' or keep_main_val == 'yes':
        keep_main = True
        break
    elif keep_main_val == 'n' or keep_main_val == 'no':
        keep_main = False
        break
    else:
        print("Please enter 'yes' or 'no'")

# Get new main sequence if needed
if(not keep_main):
    print("Which sequence is the main sequence?")
    seq_index = 0
    for seq in seqs:
        print("[{}] {}".format(seq_index, seq[1:]))
        seq_index += 1
    while True:
        try:
            main_ind = int(input("Please enter to index of the main sequence [0-{}]: ".format(seq_index - 1)))
        except ValueError:
            print("Please enter an integer")
        else:
            if main_ind >= 0 and main_ind < seq_index:
                main_seq = list(seqs)[main_ind]
                break
            else:
                print("Please enter a number from 0 to {}".format(seq_index - 1))
    
          
# Ask if names should be output
while True:
    out_names_val = input("Include names in output file? Y/n   ").lower()
    if out_names_val == 'y' or out_names_val == 'yes':
        out_names = True
        break
    elif out_names_val == 'n' or out_names_val == 'no':
        out_names = False
        break
    else:
        print("Please enter 'yes' or 'no'")

# Ask if main sequence shoudl be output
while(True):
    out_main_val = input("Include main sequence in output? Y/n   ").lower()
    if out_main_val == 'y' or out_main_val == 'yes':
        out_main = True
        break
    elif out_main_val == 'n' or out_main_val == 'no':
        out_main = False
        break
    else:
        print("Please enter 'yes' or 'no'")

  
# Find position of residues in main sequence------------------------
curr_res = 0
curr_char = 0
char_pos = []
res = {main_seq: ""}
# Search through main sequence to find char position of each residue
for c in seqs[main_seq]:
    # Check if residue
    if c != '-':
        # Check if this residue is one of interest
        if curr_res == res_ind[0]:
            # Store char position
            char_pos.append(curr_char)
            # Add to relevant sequence
            res[main_seq] += c
            # Remove residue index from search list
            del res_ind[0]
            # Check if found all residues
            if len(res_ind) == 0:
                break
        # Now looking at next residue
        curr_res += 1
    # Now looking at next character
    curr_char += 1

# Remove main sequence from sequence dictionary (seqs)
seqs.pop(main_seq, None)
#-------------------------------------------------------------------

# Pull out relevant residues from remaining sequences
for seq_name, seq_string in seqs.items():
    res[seq_name] = ""
    for char_index in char_pos:
        res[seq_name] += seq_string[char_index]

# Determine output method
print("Output methods:")
print("[0] print to screen")
print("[1] print to file")
while True:
    try:
       print_ind = int(input("Please enter the index of your chosen print method [0 or 1]: "))
    except ValueError:
        print("Input error: Please enter an integer\n")
    else:
        if print_ind == 0 or print_ind == 1:
            break
        else:
            print("Input error: Please enter 0 or 1\n")
    
# Open file if needed
if print_ind == 1:
    while True:
        try:
            f_name = input("Please enter output filename: ")
            f = open(f_name, 'w')
            break
        except OSError:
            while True:
                just_print_val = input("Invalid filename. Would you like to just print to screen instead? Y/n   ").lower()
                if just_print_val == 'y' or just_print_val == 'yes':
                    just_print = True
                    break
                elif just_print_val == 'n' or just_print_val == 'no':
                    just_print = False
                    break
                else:
                    print("Please enter 'yes' or 'no'")
            if just_print:
                print_ind = 0
                break
            
         
# Print main residues
if out_main:
    if out_names:
        if print_ind == 0:
            print(main_seq)
        else:
            f.write("{}\n".format(main_seq))
    if print_ind == 0:
        print(res[main_seq])
    else:
        f.write("{}\n".format(res[main_seq]))

# Remove main sequence from res so the rest can be printed with iteration
res.pop(main_seq, None)

# Print remaining sequences
for seq_name, res_string in res.items():
    if out_names:
        if print_ind == 0:
            print(seq_name)
        else:
            f.write("{}\n".format(seq_name))
    if print_ind == 0:
        print(res_string)
    else:
        f.write("{}\n".format(res_string))

exit()
