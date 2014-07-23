#!/usr/bin/env python

import json
import urllib2
import time

_moderators_by_subreddit_cache = {}
_moderating_subreddits_cache = {}

last_request = 0

def log(msg):
    print msg

def open_url(url):
    log("Opening %s" % url)

    global last_request
    while time.time() - last_request < 1:
        timeout = last_request - time.time() + 1
        log("Sleeping for %.3fs" % (timeout))
        time.sleep(timeout)
    last_request = time.time()

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', '/u/yawkat')]
    return opener.open(url)

def _json(url):
    return json.load(open_url(url))

def _iter_moderators(subreddit):
    log("Listing moderators of %s..." % subreddit)
    res = _json("http://api.reddit.com/r/" + subreddit + "/about/moderators")
    for u in res["data"]["children"]:
        yield str(u["name"])

def list_moderators(subreddit):
    if not subreddit in _moderators_by_subreddit_cache:
        _moderators_by_subreddit_cache[subreddit] = list(_iter_moderators(subreddit))
    return _moderators_by_subreddit_cache[subreddit]

def _skip_to(stream, s):
    if s == "":
        return True
    i = 0
    while True:
        c = stream.read(1)
        if not c:
            return False
        if c == s[i]:
            i += 1
            if i >= len(s):
                return True
        else:
            i = 0

def _iter_modded_subreddits(username):
    log("Listing modded subreddits of %s..." % username)
    try:
        f = open_url("https://pay.reddit.com/user/" + username)
    except: # 404 = banned
        return
    if _skip_to(f, '<ul id="side-mod-list">'):
        while _skip_to(f, 'href="/r/'):
            sub_name = ""
            while True:
                c = f.read(1)
                if c == '/':
                    break
                if c == "\"":
                    return
                sub_name += c
            yield sub_name

def list_modded_subreddits(username):
    if not username in _moderating_subreddits_cache:
        _moderating_subreddits_cache[username] = list(_iter_modded_subreddits(username))
    return _moderating_subreddits_cache[username]
