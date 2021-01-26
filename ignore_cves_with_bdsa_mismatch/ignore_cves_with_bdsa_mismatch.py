#!/usr/bin/env python

import argparse
import json

from blackduck.HubRestApi import HubInstance

parser = argparse.ArgumentParser(description='Ignore potentially false positive CVEs with associated BDSAs which disagree on the affected component versions within a Black Duck project version', prog='ignore_cves_with_bdsa_mismatch.py')
parser.add_argument("project_name", type=str, help='Black Duck project name')
parser.add_argument("project_version", type=str, help='Black Duck version name')
parser.add_argument("-l", "--list", help="List potential False Positive CVEs - do not marked as ignored",action='store_true')

args = parser.parse_args()

def list_projects(project_string):
	print("Available projects matching '{}':".format(project_string))
	projs = hub.get_projects(parameters={"q":"name:{}".format(project_string)})
	for proj in projs['items']:
		print(" - " + proj['name'])

def get_all_projects():
	projs = hub.get_projects()
	proj_list = []
	for proj in projs['items']:
		proj_list.append(proj['name'])
	return(proj_list)

def list_versions(version_string):
	print("Available versions:")
	vers = hub.get_project_versions(project, parameters={})
	for ver in vers['items']:
		print(" - " + ver['versionName'])

def patch_cves(version, vuln_list):
	global args

	vulnerable_components_url = hub.get_link(version, "vulnerable-components") + "?limit=9999"
	custom_headers = {'Accept':'application/vnd.blackducksoftware.bill-of-materials-6+json'}
	response = hub.execute_get(vulnerable_components_url, custom_headers=custom_headers)
	vulnerable_bom_components = response.json().get('items', [])

	active_statuses = [ "NEW", "NEEDS_REVIEW", "REMEDIATION_REQUIRED"]
	status = "IGNORED"
	comment = "Ignored as linked BDSA has component version as fixed"

	print("Processing vulnerabilities ...")
	ignoredcount = 0
	alreadyignoredcount = 0
	try:
		for vuln in vulnerable_bom_components:
			vuln_name = vuln['vulnerabilityWithRemediation']['vulnerabilityName']

			if vuln_name in vuln_list:
				if vuln['vulnerabilityWithRemediation']['remediationStatus'] in active_statuses:
					vuln['remediationStatus'] = status
					vuln['remediationComment'] = comment
					result = hub.execute_put(vuln['_meta']['href'], data=vuln)
					if result.status_code == 202:
						ignoredcount += 1
						print("{}: marked ignored".format(vuln_name))
					else:
						print("{}: Unable to change status".format(vuln_name))
				else:
					print(vuln_name + ": has BDSA which disgrees on version applicability but not active - no action")
					alreadyignoredcount += 1
			else:
				print(vuln_name + ": No action")

	except Exception as e:
		print("ERROR: Unable to update vulnerabilities via API\n" + str(e))
		return()
	print("- {} CVEs already inactive".format(alreadyignoredcount))
	print("- {} CVEs newly marked as ignored".format(ignoredcount))
	return()

hub = HubInstance()

project = hub.get_project_by_name(args.project_name)
if project == None:
	print("Project '{}' does not exist".format(args.project_name))
	list_projects(args.project_name)
	sys.exit(2)

version = hub.get_version_by_name(project, args.project_version)
if version == None:
	print("Version '{}' does not exist".format(args.project_version))
	list_versions(args.project_version)
	sys.exit(2)
else:
	print("Working on project '{}' version '{}'\n".format(args.project_name, args.project_version))

# bom_components = hub.get_version_components(version)

project_id = project['_meta']['href'].split("/")[-1]
version_id = version['_meta']['href'].split("/")[-1]

components_url = hub.get_apibase() + "/projects/" + project_id + "/versions/" + version_id + "/components?limit=9999"
custom_headers = {'Accept':'application/vnd.blackducksoftware.bill-of-materials-4+json'}
response = hub.execute_get(components_url, custom_headers=custom_headers)
components = response.json().get('items', [])

cve_list = []

num = 0
total = 0
print("Processing components:")
for comp in components:
# 	print(comp)
	print("- " + comp['componentName'] + '/' + comp['componentVersionName'])
	for x in comp['_meta']['links']:
		if x['rel'] == 'vulnerabilities':
			custom_headers = {'Accept':'application/vnd.blackducksoftware.vulnerability-4+json'}
			response = hub.execute_get(x['href'] + "?limit=9999", custom_headers=custom_headers)
			vulns = response.json().get('items', [])
			for vuln in vulns:
				total += 1
				if vuln['source'] == 'NVD':
					for x in vuln['_meta']['links']:
						if x['rel'] == 'related-vulnerabilities':
							if x['label'] == 'BDSA':
# 								print("{} has BDSA which disagrees with component version - potential false positive".format(vuln['name']))
								if vuln['name'] not in cve_list:
									cve_list.append(vuln['name'])
								num += 1

print("Found {} total vulnerabilities".format(total))
print("Found {} CVEs with associated BDSAs but which do not agree on affected component version\n".format(num))

print(cve_list)

if not args.list:
	patch_cves(version, cve_list)
