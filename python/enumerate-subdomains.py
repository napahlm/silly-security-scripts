import requests
import sys

sub_list = open("wordlist.txt").read() # list with line-separated domains
subdomains = sub_list.splitlines()       # string1\nstring2 -> ["string1", "string2"]

for sub in subdomains:
    sub_domains = f"http://{sub}.{sys.argv[1]}"

    try:
        requests.get(sub_domains)
    except requests.ConnectionError:
        pass

    else:
        print("Valid domain: ", sub_domains)