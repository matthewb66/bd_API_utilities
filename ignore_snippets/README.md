# Synopsys Black Duck - ignore_snippets.py
# OVERVIEW

This script is provided under an OSS license (specified in the LICENSE file) to allow users to report and manage unconfirmed snippets within a Black Duck project version.

It does not represent any extension of licensed functionality of Synopsys software itself and is provided as-is, without warranty or liability.

# DESCRIPTION

The script will either report or ignore/unignore unconfirmed snippets for a specific project version based on supplied criteria. Confirmed snippets will be unaffected by using this script.

It is intended to batch process unconfirmed snippet matches, ignoring snippets below certain levels to reduce the manual effort of confirming the remainder of unconfirmed snippets.

The script uses the `hub-rest-api-python` package to access the Black Duck APIs (see prerequisites to install and configure this package).

The project name and version need to be specified. If the project name is not matched in the server then a list of projects matching the supplied project string will be displayed (and the script will terminate). If the version name is not matched for the specified project, then a list of all versions will be displayed (and the script will terminate).

The default operation is only to list unconfirmed, unignored snippets. Options are available to specify criteria for ignoring/unignoring unconfirmed snippets or to list all unconfirmed snippets including those already ignored.

# PREREQUISITES

Please refer to the requirements in the top README for this repo. This script uses the `hub-rest-api-python` package which must be pre-installed and configured.

# USAGE

The `ignore_snippets.py` script can be invoked as follows:

    Usage: ignore_snippets.py [-h] [-c COVERAGEMIN] [-z SIZEMIN]
                              [-l MATCHEDLINESMIN] [-i] [-u] [-a]
                              project_name project_version

    Report or ignore/unignore unconfirmed snippets in the specified project/version using
    the supplied criteria. Running with no options apart from project and version will
    report all snippets not currently ignored (use --all option to process all
    snippets including currently ignored).

    Required arguments:
      project_name          Black Duck project name
      project_version       Black Duck version name

    Optional arguments:
      -h, --help            show this help message and exit
      -i, --ignore          Ignore matched snippets
      -u, --unignore        Unignore matched snippets (undo ignore action)
      -a, --all             Process/report all snippets including currently
                            ignored
      -c COVERAGEMIN, --coveragemin COVERAGEMIN
                            Minimum matched lines percentage (1-100)
      -z SIZEMIN, --sizemin SIZEMIN
                            Minimum source file size (in bytes)
      -l MATCHEDLINESMIN, --matchedlinesmin MATCHEDLINESMIN
                            Minimum number of matched lines in snippet from source
                            file

If `project_name` does not match a single project then all matching projects will be listed and the script will terminate.

If `project_version` does not match a single project version then all matching versions will be listed for the specified project and the script will terminate.

The `-a` or `--all` option will cause all unconfirmed snippets to be listed/processed (default is to only report/process unconfirmed snippets not currently ignored).

The `-i` or `--ignore` option will ignore unconfirmed snippets matching the criteria.

The `-u` or `--unignore` option will UNignore unconfirmed snippets matching the criteria.

The `-c COVERAGEMIN` or `--coveragemin COVERAGEMIN` sets the filter based on the percentage coverage value (percentage of matched lines) with snippets below the value being processed.

The `-z SIZEMIN` or `--sizemin SIZEMIN` sets the filter based on the filesize in bytes with snippets below the value being processed.

The `-l MATCHEDLINESMIN` or `--matchedlinesmin MATCHEDLINESMIN` sets the filter based on the number of lines matched with snippets below the value being processed.

# EXAMPLE OUTPUT

Running the script with the following options `python3 ignore_snippets.py snip1 1.0 --all --matchedlinesmin 100` (and with an existing snip1 project and 1.0 version) would create a list of unconfirmed snippet matches (including previously ignored ones) and whether they would be subsequently ignored if the `--ignore` option was used:

    Working on project 'hello_world' version 'Default Detect Version'

    Listing all Unconfirmed Snippets - using Coverage = Any, Size = Any, Lines Matched = 100

         SIZE (bytes)  BLOCK  COVERAGE%  MATCHLINES  STATUS                ACTION              
    /esp8266-frankenstein-6ed48eedb2166ad20611b24ee2b4e4e229357051/coverity_configs/g++cc-config-1/coverity-compiler-compat.h
            1,018,162      1         52          39  Not ignored           Would be ignored    
    /cbmc-cbmc-5.8/src/ansi-c/coverity-compiler-compat.h
            1,018,162      2          1          26  Not ignored           Would be ignored     
    /cbmc-cbmc-5.8/src/ansi-c/coverity-compiler-compat.h
            1,015,861      2          1          26  Not ignored           Would be ignored    
    /cbmc-cbmc-5.8/src/ansi-c/coverity-compiler-compat.h
            1,016,006      2          1          26  Not ignored           Would be ignored    
    /esp8266-frankenstein-6ed48eedb2166ad20611b24ee2b4e4e229357051/coverity_configs/g++cc-config-1/coverity-compiler-compat.h
            1,016,006      1         52          39  Not ignored           Would be ignored    
    /cbmc-cbmc-5.8/src/ansi-c/coverity-compiler-compat.h
            1,016,006      2          1          26  Not ignored           Would be ignored     
    /cbmc-cbmc-5.8/src/ansi-c/coverity-compiler-compat.h
            1,015,861      2          1          26  Not ignored           Would be ignored    

    7 Total unconfirmed snippets in project (0 ignored already)
    0 snippets Ignored
