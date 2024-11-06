import csv
import json


class EvidenceReader:

  def __init__(self):
    self.evidence_json = None

  def convert_csv_to_json(self):
    data = []
    with open("evidence.csv", 'r') as csvfile:
      csv_reader = csv.DictReader(csvfile)
      for row in csv_reader:
        data.append(row)

    with open("evidence.json", 'w') as jsonfile:
      json.dump(data, jsonfile, indent=4)
