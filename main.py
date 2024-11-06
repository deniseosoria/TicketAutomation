from jira_updater import JiraUpdater
from evidence_reader import EvidenceReader

if __name__ == "__main__":
  evidence_reader = EvidenceReader()
  evidence_reader.convert_csv_to_json()

  jira_updater = JiraUpdater()
  jira_updater.update_jira()

# Denise = denise.osoria@jjay.cuny.edu -> 192.168.1.166
# Deycie Hilario = deycie.hilario@jjay.cuny.edu -> 192.168.1.1
# Michael F = MICHAEL.FIORUCCI13@student.qcc.cuny.edu -> 192.168.1.126
# joudy.sherif@jjay.cuny.edu -> 192.168.1.211
