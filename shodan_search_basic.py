#!/usr/bin/env python
#
# shodan_ips.py
# Search SHODAN and print a list of IPs matching the query
#
# Author: achillean

import sys

import shodan

# Configuration
API_KEY = "stCZJCupO5DovLErnPjLe7a75hhchJPW"

# Input validation
if len(sys.argv) == 1:
        print('Usage: %s <search query>' % sys.argv[0])
        sys.exit(1)

try:
        # Setup the api
        api = shodan.Shodan(API_KEY)

        # Perform the search
        query = ' '.join(sys.argv[1:])
        result = api.search(query)

        # Loop through the matches and print each IP
        for service in result['matches']:
                print(service['ip_str'])
except Exception as e:
        print('Error: %s' % e)
        sys.exit(1)