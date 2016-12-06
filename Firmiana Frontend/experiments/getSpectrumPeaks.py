from views import*

filename = "searchId.txt"
peptide_spectrums = 0
num_spectrums = 0

with open(filename, "r") as f:
    lines = f.readlines()
    for line in lines:
        searchId = int(line)
        gardener_search_info = 0
