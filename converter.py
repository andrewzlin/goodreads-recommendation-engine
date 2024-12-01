import csv
import json

with open('books.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    json_data = []
    for row in csv_reader:
        json_data.append(row)

json_string = json.dumps(json_data)

with open('books.json', 'w') as json_file:
    json_file.write(json_string)