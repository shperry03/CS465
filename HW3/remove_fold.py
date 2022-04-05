import csv

with open('actions.csv', 'rb') as inp, open('first_edit.csv', 'wb') as out:
    writer = csv.writer(out)
    i = 0
    for row in csv.reader(inp):
        if row[0] == "0":
            i = i + 1
            if(i%2 == 0):
                writer.writerow(row)
                print(row)
        else:
            writer.writerow(row)
