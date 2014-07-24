#!/usr/bin/env python

import api
import argparse
import json
import sys

def find_links(subreddit):
    links = {}
    for mod in api.list_moderators(subreddit):
        if mod == "AutoModerator":
            continue
        for sub in api.list_modded_subreddits(mod):
            if not sub in links:
                links[sub] = 0
            links[sub] += 1
    return links

parser = argparse.ArgumentParser()
parser.add_argument("subreddit", type=str)
parser.add_argument("--output", choices=("json","table"))
parser.add_argument("--loglevel", choices=("verbose", "status_error", "quiet"), default="status_error")
args = parser.parse_args()

if args.loglevel == "verbose":
    api.log = lambda msg: (sys.stdout.write(msg + "\n"))
if args.loglevel == "status_error":
    api.log = lambda msg: (sys.stderr.write("%80s\r" % msg))
if args.loglevel == "quiet":
    api.log = lambda msg: ()

result = find_links(args.subreddit)
if args.loglevel == "status_error":
    print "%40s" % ""
if args.output == "json":
    print json.dumps(result)
else:
    for k in sorted(result.keys(), key=lambda k: -result[k]):
        print "%30s%6s" % (k, result[k])
