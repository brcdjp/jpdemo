# -*- coding: utf-8 -*-
from st2actions.runners.pythonrunner import Action
import datetime
from redmine import Redmine
class NewTicket(Action):
    def run(self, subject, description):
        rm = Redmine('http://172.24.199.111/', key='6cd5f81bd01aeb6a31d2504d54366a215f34273e')
        issue = rm.issue.new()
        issue.project_id = 'test'
        issue.subject = subject
        issue.tracker_id = 1
        issue.description = description
        issue.status_id = 1
        issue.priority_id = 1
        issue.assigned_to_id = 1
        #issue.watcher_user_ids = [1,3]
        #issue.parent_issue_id = 
        now = datetime.date.today()
        issue.start_date = now #開始日
        issue.due_date = now + datetime.timedelta(days=1)   #期日
        issue.estimated_hours = 4
        issue.done_ratio = 40
        #issue.custom_fields = [{'id': 1, 'value': 'foo'}]
        #issue.uploads = [{'path': '/share/test.txt'}]
        issue.save()
        return (True, subject)
