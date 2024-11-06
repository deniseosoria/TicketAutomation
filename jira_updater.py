from jira import JIRA
import os
import json
from datetime import datetime, timedelta
import hashlib


class JiraUpdater:

  def __init__(self):
    try:
      server = "https://capstone2-project.atlassian.net"
      self.jira = JIRA(server,
                       basic_auth=(os.environ['JIRA_EMAIL'],
                                   os.environ['JIRA_TOKEN']))
    except Exception as e:
      raise Exception(e)

    with open('evidence.json') as f:
      self.evidence_json = json.load(f)

    with open('assignees.json') as f:
      self.assignees_json = json.load(f)

    self.existing_evidence = set()

  def read_existing_evidence(self):
    for evidence in self.evidence_json:
      id = self.generate_id(evidence["Plugin ID"], evidence["Host"])
      self.existing_evidence.add(id)

  def calculate_due_date(self, evidence):
    today = datetime.today()
    risk = evidence["Risk"].lower()

    if risk == "critical":
      duration = timedelta(days=10)
    elif risk == "high":
      duration = timedelta(days=30)
    elif risk == "medium":
      duration = timedelta(days=60)
    elif risk == "low":
      duration = timedelta(days=180)
    else:
      duration = timedelta(days=30)

    due_date = today + duration

    return due_date

  def generate_id(self, plugin_id, ip_address):
    return hashlib.md5(f"{plugin_id}{ip_address}".encode("utf-8")).hexdigest()

  def update_jira(self):
    self.read_existing_evidence()
    self.existing_evidence.clear()
    tickets_resolved = self.resolve_tickets()
    tickets_created, tickets_updated = self.create_tickets()

    print(f"Tickets Created: {tickets_created}")
    print(f"Tickets Resolved: {tickets_resolved}")
    print(f"Tickets Already Exist: {tickets_updated}")

  def issue_exists_in_jira(self, id):
    issues = self.jira.search_issues(f'project = "SEC" and labels = "id:{id}"')

    if len(issues) > 0:
      return True
    else:
      return False

  def get_assignee(self, evidence):
    #get ip address from evidence
    ip_address = evidence["Host"]
    #using the ip address from the assignee.json file, get the corresponding assignee (email)
    assignees_email = self.assignees_json[ip_address]

    #return it
    return assignees_email

  def resolve_tickets(self):
    issues_resolved = 0

    outstanding_issues = self.jira.search_issues('project = "SEC"',
                                                 startAt=0,
                                                 maxResults=1000)

    for issue in outstanding_issues:
      for label in issue.fields.labels:
        if "id" in label:
          id = label.replace("id", "")

      if not id in self.existing_evidence:
        self.jira.transition_issue(issue, transition="Done")
        issues_resolved += 1

    return issues_resolved

  def create_tickets(self):
    #fields = self.create_ticket_fields("test")
    #test_ticket = self.jira.create_issue(fields)

    issues_created = 0
    issues_updated = 0

    for evidence in self.evidence_json:
      plugin_id = evidence["Plugin ID"]
      cve = evidence["CVE"]
      cvss_v2 = evidence["CVSS v2.0 Base Score"]
      risk = evidence["Risk"]
      host = evidence["Host"]
      protocol = evidence["Protocol"]
      port = evidence["Port"]
      name = evidence["Name"]
      synopsis = evidence["Synopsis"]
      description = evidence["Description"]
      solution = evidence["Solution"]
      see_also = evidence["See Also"]
      plugin_output = evidence["Plugin Output"]

      id = self.generate_id(plugin_id, host)

      ticket_title = f"{plugin_id} - {name}"
      ticket_description = (f'''
        *Host:* {host}\n
        *Protocol:* {protocol}\n
        *Port:* {port}\n
        *Description:* {description}\n
        *Solution:* {solution}
        ''')

      if risk.lower() == "critical":
        risk = "Highest"

      fields = {
        "project":
        "SEC",
        "issuetype":
        "Task",
        "summary":
        ticket_title,
        "description":
        ticket_description,
        "labels": [f'id:{id}'],
        "duedate":
        self.calculate_due_date(evidence).strftime("%Y-%m-%d %H:%M:%S"),
        "priority": {
          "name": risk
        },
        "assignee": {
          "accountId": self.get_assignee(evidence)
        }
      }

      if self.issue_exists_in_jira(id):
        issues_updated += 1
      else:
        self.jira.create_issue(fields)

    return issues_created, issues_updated
