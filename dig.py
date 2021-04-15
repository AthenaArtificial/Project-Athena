#opens the given file and eliminates for numbers
with open('filename.txt') as f:
    data = ''.join(i for i in f.read() if not i.isdigit())

#opens another file to print the updated script
with open('filename1.txt', 'w') as f:
    f.write(data)