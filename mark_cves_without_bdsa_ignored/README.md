# Synopsys Black Duck - ignore_cves_with_bdsa_mismatch.py
# OVERVIEW

This script is provided under an OSS license (specified in the LICENSE file) to allow users to ignore potentially false positive CVEs with associated BDSAs which disagree on the affected component versions within a Black Duck project version.

It does not represent any extension of licensed functionality of Synopsys software itself and is provided as-is, without warranty or liability.

# DESCRIPTION

The script will (list or) ignore potentially false positive CVEs with associated BDSAs which disagree on the affected component versions within a Black Duck project version.

CVEs from the NVD commonly have 'catch-all' component version ranges (for example all versions up to 2.9), however vulnerabilities are typically introduced in a specific version (e.g. version 1.92), and fixes are applied to parallel branches, so in this example the actual affected version range could be v1.92 to 2.9 excepting 2.6 and 2.8_beta. BDSA records are analysed by security professionals who identify the full list of affected versions, and there is often a disagreement between the CVE and BDSA affected version range, with BDSA being more accurate and authoritative.

This script identifies (and ignores) CVEs with matching BDSAs but where only the CVE is associated to component versions in a Black Duck project version Bill or Materials.

The script uses the `hub-rest-api-python` package to access the Black Duck APIs (see prerequisites to install and configure this package).

The project name and version need to be specified. If the project name is not matched in the server then a list of projects matching the supplied project string will be displayed (and the script will terminate). If the version name is not matched for the specified project, then a list of all versions will be displayed (and the script will terminate).

Use the `--list` option to show affected CVEs without ignoring.

# PREREQUISITES

Please refer to the requirements in the top README for this repo. This script uses the `hub-rest-api-python` package which must be pre-installed and configured.

# USAGE

The `ignore_cves_with_bdsa_mismatch.py` script can be invoked as follows:

    usage: ignore_cves_with_bdsa_mismatch.py [-h] [-l]
                                             project_name project_version

    ignore potentially false positive CVEs with associated BDSAs which disagree on
    the affected component versions within a Black Duck project version

    positional arguments:
      project_name     Black Duck project name
      project_version  Black Duck version name

    optional arguments:
      -h, --help       show this help message and exit
      -l, --list       List potential False Positive CVEs - do not marked as
                       ignored

If `project_name` does not match a single project then all matching projects will be listed and the script will terminate.

If `project_version` does not match a single project version then all matching versions will be listed for the specified project and the script will terminate.

The `-l` or `--list` option will list all affected CVEs without ignoring them.
