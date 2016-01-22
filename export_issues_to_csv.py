#!/usr/bin/env python
"""
Generate CSV of open Github issues for OpenElections

USAGE:
    # Create a Github API token and set the GITHUB_API_TOKEN environment 
    # variable locally

    # Then run the script (output in reports)
    python export_issues_to_csv.py

"""
import csv
import datetime
import os
import sys

from github3 import login


try:
    GITHUB_API_TOKEN = os.environ['GITHUB_API_TOKEN']
except KeyError:
    sys.exit("You must set an environment variable for GITHUB_API_TOKEN!")

def repos():
    """Return repos as iterator"""
    gh = login(token=GITHUB_API_TOKEN)
    return gh.organization('openelections').repositories()

def build_row_for_export(repo, issue, headers):
    labels = ';'.join([label.name for label in issue.labels()])
    data = (
        repo.name,
        issue.number,
        issue.title,
        labels,
        issue.html_url,
        issue.created_at.isoformat(),
        issue.updated_at.isoformat()
    )
    return dict(zip(headers, data))

def main():
    headers = ('repo','issue_num','title','labels', 'url', 'created', 'updated')
    timestamp = datetime.date.today().isoformat()
    outfile = 'reports/openelex_issues_{}.csv'.format(timestamp)
    with open(outfile, 'wb') as report:
        print "Creating {}...".format(outfile)
        writer = csv.DictWriter(report, fieldnames=headers, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for repo in repos():
            print "Compiling issues for {}...".format(repo.name)
            for issue in repo.issues('open'):
                row = build_row_for_export(repo, issue, headers)
                writer.writerow(row)

if __name__ == '__main__':
    main()
