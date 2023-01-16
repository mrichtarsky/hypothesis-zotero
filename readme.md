# Zotero-Hypothesis Importer #

Based on https://github.com/JD-P/hypothesis-zotero. Differences:
- Only one note per Zotero item is created, with all Hypothesis notes contained therein.
- No GUI

## Introduction ##

This program scans through a [Zotero](https://zotero.com) library and checks
each URL for [Hypothesis](https://hypothes.is) annotations. If annotations are
found it imports them into the Zotero library as note objects with their
associated tags.

## Usage ##

Create `settings.py` with this content:

```
# The userID for your Zotero API usage, available here: https://www.zotero.org/settings/keys
library_id = ''

# A developer API key for Zotero, you can make one here: https://www.zotero.org/settings/keys/new
zot_api_key = ''

# Your Hypothesis username, which should just be the username you use to access the service.
hyp_username = ''

# Your Hypothesis Developer API key, available here: https://hypothes.is/account/developer
hyp_api_key = ''

# Number of items to grab from Zotero.
num2grab = 1000
```

Then run `hypothesis_zotero.py`.
