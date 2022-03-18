# format_fasta_for_MED
This script will edit fasta headers in an alignment file as is required by the oligoptying/MED pipeline. 
This script is a continuation of a script that edits fasta headers in an alignment file for constructing newick string. 

Please note that the function for formating fasta headers specifically for MED/oligotyping can be used on it's own by simply importing the function from this script. An even more important note, you will need to edit this script depending on the naming convention used for your samples.


One more note, this script needs to be edited by me, in that you will not be using reference sequences from a database such as NCBI during the oligotyping/MED pipeline. This will likely not cause any problems, and can be ignored almost completely, but if you run into any problems, please let me know.
