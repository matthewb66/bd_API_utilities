#!/usr/bin/env python

import argparse
import json
import sys

from blackduck.HubRestApi import HubInstance

def get_snippet_entries(hub, project_id, version_id, limit=1000, offset=0):
	hub._check_version_compatibility()
	paramstring = "?limit=" + str(limit) + "&offset=" + \
		str(offset) + "&filter=bomMatchType:snippet&filter=bomMatchReviewStatus:not_reviewed"
	# Using internal API - see https://jira.dc1.lan/browse/HUB-18270: Make snippet API calls for ignoring, confirming snippet matches public
	path =  "{}/internal/projects/{}/versions/{}/source-bom-entries".format(hub.get_apibase(), project_id, version_id)
	url = path + paramstring
	#print(url)
	response = hub.execute_get(url)
	jsondata = response.json()
	return jsondata

def ignore_snippet_bom_entry(hub, hub_project_id, hub_version_id, snippet_bom_entry, ignore):

	hub._check_version_compatibility()

	if ignore:
		post_body = '{ "ignored": true }'
	else:
		post_body = '{ "ignored": false }'

	scanid = snippet_bom_entry['scanId']
	nodeid = snippet_bom_entry['compositeId']
	snippetid = snippet_bom_entry['fileSnippetBomComponents'][0]['hashId']
	url = "{}/projects/{}/versions/{}/scans/{}/nodes/{}/snippets/{}".format(hub.get_apibase(), hub_project_id, hub_version_id, scanid, nodeid, snippetid)
# 	print(url)

	response = hub.execute_put(url, post_body)
	return(response.ok)


parser = argparse.ArgumentParser(description='Report or ignore/unignore unconfirmed snippets in the specified project/version using supplied options. Running with no options apart from project and version will report all snippets not currently ignored (use --all option to process all snippets including currently ignored).', prog='ignore_snippets.py')
parser.add_argument("project_name", type=str, help='Black Duck project name')
parser.add_argument("project_version", type=str, help='Black Duck version name')
#parser.add_argument("-s", "--scoremin", type=int, default=101, help='Minimum match score percentage value (hybrid value of snippet match and likelihood that component can be copied)')
parser.add_argument("-c", "--coveragemin", type=int, default=101, help='Minimum matched lines percentage (1-100)')
parser.add_argument("-z", "--sizemin", type=int, default=1000000000, help='Minimum source file size (in bytes)')
parser.add_argument("-l", "--matchedlinesmin", type=int, default=1000000, help='Minimum number of matched lines in snippet from source file')
parser.add_argument("-i", "--ignore", action='store_true', help='Ignore matched snippets')
parser.add_argument("-u", "--unignore", action='store_true', help='Unignore matched snippets (undo ignore action)')
parser.add_argument("-a", "--all", action='store_true', help='Process/report all snippets including currently ignored')

args = parser.parse_args()

def list_projects(project_string):
	print("Available projects matching '{}':".format(project_string))
	projs = hub.get_projects(parameters={"q":"name:{}".format(project_string)})
	count = 0
	for proj in projs['items']:
		print(" - " + proj['name'])
		count += 1
	if count == 0:
		print(" - None")

def get_all_projects():
	projs = hub.get_projects()
	proj_list = []
	for proj in projs['items']:
		proj_list.append(proj['name'])
	return(proj_list)

def list_versions(version_string):
	print("Available versions:")
	vers = hub.get_project_versions(project, parameters={})
	count = 0
	for ver in vers['items']:
		print(" - " + ver['versionName'])
		count += 1
	if count == 0:
		print(" - None")

hub = HubInstance()

project = hub.get_project_by_name(args.project_name)
if project == None:
	print("Project '{}' does not exist".format(args.project_name))
	list_projects(args.project_name)
	sys.exit(2)

version = hub.get_version_by_name(project, args.project_version)
if version == None:
	print("Project '{}' Version '{}' does not exist".format(args.project_name, args.project_version))
	list_versions(args.project_version)
	sys.exit(2)
else:
	print("Working on project '{}' version '{}'\n".format(args.project_name, args.project_version))

project_id = project['_meta']['href'].split("/")[-1]
version_id = version['_meta']['href'].split("/")[-1]

if args.unignore:
	ignorestr = "Unignored"
else:
	ignorestr = "Ignored"
#print(version_id)

if args.coveragemin == 101:
    covstring = "Any"
else:
    covstring = "{}".format(args.coveragemin)
if args.sizemin == 1000000000:
    sizestring = "Any"
else:
    sizestring = "{}".format(args.sizemin)
if args.matchedlinesmin == 1000000:
    linesstring = "Any"
else:
    linesstring = "{}".format(args.matchedlinesmin)

if args.ignore or args.unignore:
    print("Processing Unconfirmed Snippets matching Coverage = {}, Size = {}, Lines Matched = {}\n".format(covstring, sizestring, linesstring))
elif args.all:
    print("Listing all Unconfirmed Snippets - using Coverage = {}, Size = {}, Lines Matched = {}\n".format(covstring, sizestring, linesstring))
else:
    print("Listing all Unconfirmed, Not Ignored Snippets - using Coverage = {}, Size = {}, Lines Matched = {}\n".format(covstring, sizestring, linesstring))

print("{:40} {:12} {:5} {:10} {:13}  {:20} {:20}".format("FILE", "SIZE (bytes)", "BLOCK", "COVERAGE %", "MATCHED LINES", "STATUS", "ACTION"))
ignoredcount = 0
alreadyignored = 0
snippet_bom_entries = get_snippet_entries(hub, project_id, version_id)
if snippet_bom_entries:
    #print(snippet_bom_entries)
    for snippet_item in snippet_bom_entries['items']:
        blocknum = 1
        for match in snippet_item['fileSnippetBomComponents']:
            if match['ignored']:
                alreadyignored += 1
            if not args.all and match['ignored'] != args.unignore:
                continue
            #print(json.dumps(match, indent=4))

            if match['ignored']:
                igstatus = "Ignored"
            else:
                igstatus = "Not ignored"
            matchedlines = match['sourceEndLines'][0] - match['sourceStartLines'][0]
            if (int(match['matchCoverage']) < int(args.coveragemin)) and (int(snippet_item['size']) < int(args.sizemin)) and (matchedlines < int(args.matchedlinesmin)):
                if not (args.ignore or args.unignore):
                    print("{:40} {:>12,d} {:5} {:10} {:13}  {:20} {:20}".format(snippet_item['name'], snippet_item['size'], blocknum, match['matchCoverage'], matchedlines, igstatus, "Would be ignored"))
                else:
                    if ignore_snippet_bom_entry(hub, project_id, version_id, snippet_item, not(args.unignore)):
                        print("{:40} {:>12,d} {:5} {:10} {:13}  {:20} {:20}".format(snippet_item['name'], snippet_item['size'], blocknum, match['matchCoverage'], matchedlines, igstatus, ignorestr))
                        ignoredcount += 1
                    else:
                        print("File: {:40} , Block {}: Could not ignore (API Error)".format(snippet_item['name'], blocknum))
            elif not (args.ignore or args.unignore):
                print("{:40} {:>12,d} {:5} {:10} {:13}  {:20} {:20}".format(snippet_item['name'], snippet_item['size'], blocknum, match['matchCoverage'], matchedlines, igstatus, "Would not be ignored"))
            blocknum += 1
    print("\n{} Total Files with unconfirmed snippets in project ({} ignored already)".format(len(snippet_bom_entries['items']), alreadyignored))
    print("{} snippets {}".format(ignoredcount, ignorestr))
