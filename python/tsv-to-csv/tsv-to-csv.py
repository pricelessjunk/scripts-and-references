#!/usr/bin/python3

f = open("list.txt", "r")

ids = []
emails = []

for line in f:
    line = line.split("\t")
    line[1] = line[1].replace("\n", "")
    line[1] = line[1].replace(" ", "")
    ids.append(line[0])
    emails.append(line[1])

ids = ",".join(ids)
emails = ",".join(emails)

print("Ids in CSV -")
print(ids)
print("emails in CSV -")
print(emails)

f.close()
