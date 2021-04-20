########################
######  AthenaAI  ######
######    2021    ######
########################
### Text Processing ####
########################


input_path = "../Authors/Plato/Raw/CRITIAS.txt"
output_path = "../Authors/Plato/Processed/"

# name : length
names = {"Theodorus. ": 11,
         "Socrates. ": 10,
         "Theaetetus. ": 12,
         "Stranger. ": 10,
         "Theod. ": 7,
         "Soc. ": 5,
         "Y. Soc. ": 8,
         "Theaet. ": 8,
         "Str. ": 5,
         "Protarchus. ": 12,
         "Pro. ": 5,
         "Philebus. ": 10,
         "Phi. ": 5,
         "Critias. ": 9,
         "Crit. ": 6,
         "Timaeus. ": 9,
         "Tim. ": 5,
         "Hermocrates. ": 13
         }

"""Read and process raw"""
output_text_list = []
new_conv = ""
with open(input_path, "r") as file:
    for line in file:
        # Leading and trailing spaces
        line = line.strip()
        is_new_para = False

        n = ""
        for name in names:
            if name in line:
                n = name
                is_new_para = True

        if is_new_para == True:
            if len(new_conv) > 100:
                output_text_list.append(new_conv)
            new_conv = ""
            new_conv += line[names[n]:]
        else:
            is_new_para = False
            line = " " + line
            new_conv += line


"""Append to a new text file"""
with open(output_path + "Plato.txt", "a") as file:
    for conv in output_text_list:
        file.write(conv)