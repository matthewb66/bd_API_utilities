# Black Duck API utilities

Various API scripts for Black Duck - for use alongside the hub_rest_api_python package

# PREREQUISITES

All scripts have the following requirements:

1. Python 3 must be installed.

1. Install the following packages in the virtualenv:

       pip install blackduck

1. An API key for the Black Duck server must be configured within the `.restconfig.json` file in the script invocation folder - see the `CONFIG FILE` section below.

# CONFIG FILE

Configure the Black Duck connection within the `.restconfig.json` file in the script invocation folder - example contents:

    {
      "baseurl": "https://myhub.blackducksoftware.com",
      "api_token": "YWZkOTE5NGYtNzUxYS00NDFmLWJjNzItYmYwY2VlNDIxYzUwOmE4NjNlNmEzLWRlNTItNGFiMC04YTYwLWRBBWQ2MDFXXjA0Mg==",
      "insecure": true,
      "debug": false
    }

# SCRIPTS IN THIS REPO

[ignore_snippets.py](https://github.com/matthewb66/bd_API_utilities/tree/main/ignore_snippets) - Batch process unconfirmed snippets to ignore those below specified criteria

[mark_cves_without_bdsa_ignored.py](https://github.com/matthewb66/bd_API_utilities/tree/main/mark_cves_without_bdsa_ignored) - Batch process CVEs to ignore those within a project version with an associated BDSA but which disagrees on the affected component version (ignoring potentially false positive CVEs due to poor version association).
