#Author: Sam Czerski
#Date: 3/9/2022
#Description: This script takes input as a multiple sequence
#alignment file (eg. otu_45_anaerococcus.aln) and remove extra
#header info for constructing a tree in newick format. Additionally, this scripts
#creates another alignment file with fasta headers formatted correctly for oligotyping and MED
#*****NOTE*****: this script is specifically for dealing with the Pelton group samples.
#there are problems with sample ID's outlined before and will need to be addressed before automation can happen.
#this is already annoying since the pelton group didn't give uid's when the samples were processed. I can hopefully change labels on figures downstream if necessary.

#imports
import glob

#Takes the OTU fasta file as input and returns a fasta file of filtered records based on a chosen "size" parameter
def remove_extra_header_info(alignment_file):
    handles = open(alignment_file, "r")
    handles_list = []
    for line in handles:
        if line.startswith(">"):
            handles_list.append(line)

    handles.close()
    edit_headers(handles_list)
    format_header_for_oligo(handles_list)



def edit_headers(handles_list):
    new_headers = []
    ncbi_headers = []
    pacbio_headers = []

    for element in handles_list:
        if element.startswith(">m"):
            handle_id_items = element.split(sep=';')
            pacbio_headers.append(handle_id_items[0])

        elif element.startswith(">NR"):
            handle_id_items = element.split(sep=' ')
            ncbi_headers.append(handle_id_items[0])

    handles = open(aln_file[0], "r")
    i = 0
    j = 0
    with open("otu_alignment_w_edited_header.aln", "w") as fr:
        for line in handles:
            if line.startswith(">m") == True:
                fr.write(line.replace(str(line), pacbio_headers[i]) + "\n")
                i+=1
            elif line.startswith(">NR") == True:
                #fr.write(">" + line.replace(str(line), ncbi_headers[j]) + "\n")
                fr.write(line.replace(str(line), ncbi_headers[j]) + "\n")
                j+=1
            else:
                fr.write(line)
#RIGHT NOW, THE ID I WANT AS THE HEADER IS BEING ADDED TO THE FIRST LINE OF THE ALIGNMENT AND THE OLD HEADER IS NOT REPLACED...
    #NEED TO FIGURE OUT HOW TO FIX THIS.
    handles.close()

    return new_headers

def format_header_for_oligo(handles_list):
    new_headers = []
    ncbi_headers = []
    pacbio_headers = []

    for element in handles_list:
        if element.startswith(">m"):
            handle_id_items = element.split(sep=';')
            #pacbio_headers.append(handle_id_items[1])
            handle_id_item_id = handle_id_items[1].split(sep="=")
            #now I need to replace the "_" with "-" in the sample id
            #handle_id_item_id[1] holds the sample id
            #*******this is going to be tricky. In order to automate this eventually, the sample id naming convention is going to need to be predicted.
            #****this instance is particularly annoying because we recieved the uid's much later after the processing was done, so there is a mix of ID's.
            handle_id_parts = handle_id_item_id[1].split(sep="_")
            if len(handle_id_parts) == 2:
                handle_id_w_dash = handle_id_parts[0] + '-' + handle_id_parts[1]
            elif len(handle_id_parts) == 1:
                #no dash is actually here, these are just numeric values because that is how the samples were named at the time of processing
                handle_id_w_dash = handle_id_parts[0]
            #I need something to differentiate reads associated with the same sample
            unique_identifiers = element.split(sep='/')
            handle_unique_identifier = unique_identifiers[1]

            #create the new header and append to the list for reformatting
            oligo_header = ">" + handle_id_w_dash + "_" + handle_unique_identifier
            pacbio_headers.append(oligo_header)

        elif element.startswith(">NR"):
            handle_id_items = element.split(sep=' ')
            handle_id_item_id = handle_id_items[0].split(sep="_")
            handle_id_num = handle_id_item_id[1]
            #these ID's are unique and should only be associated with one read, unlike the pacbio reads, so I don't need a unique identifer.
            oligo_header = "NR-" + handle_id_num + "_1"
            ncbi_headers.append(oligo_header)

    handles = open(aln_file[0], "r")
    i = 0
    j = 0
    with open("otu_alignment_for_oligotyping.aln", "w") as fr:
        for line in handles:
            if line.startswith(">m") == True:
                fr.write(line.replace(str(line), pacbio_headers[i]) + "\n")
                i += 1
            elif line.startswith(">NR") == True:
                fr.write(">" + line.replace(str(line), ncbi_headers[j]) + "\n")
                j += 1
            else:
                fr.write(line)
    # RIGHT NOW, THE ID I WANT AS THE HEADER IS BEING ADDED TO THE FIRST LINE OF THE ALIGNMENT AND THE OLD HEADER IS NOT REPLACED...
    # NEED TO FIGURE OUT HOW TO FIX THIS.
    handles.close()

    return new_headers

#main function
if __name__ == '__main__':
    #Get Input
    aln_file = glob.glob("*.aln")
    remove_extra_header_info(aln_file[0])
    print("\nFasta headers for tree building have been edited and wrote to otu_alignment_w_edited_header.aln")
    print("\nFasta headers for oligotyping and minimum entropy decomposition have been reformatted and wrote to otu_alignment_for_oligotyping.aln")
    print("\nFin")
