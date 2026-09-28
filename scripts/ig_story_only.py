#!/usr/bin/env python3
"""Story-ONLY Instagram publisher for _assetrama (story-only slots, Ram's
approved cadence 28/09/2026: premarket/moneystory/geopolitics post no reel).
Usage: python ig_story_only.py TOKEN_FILE STORY_VIDEO_URL"""
import json, sys, time, urllib.request, urllib.parse, urllib.error
IG_ID = "17841405587045840"
API = "https://graph.instagram.com/v23.0"
def post(url, data, token):
    data = dict(data, access_token=token)
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try: return json.loads(e.read())
        except Exception: return {"_http_error": e.code}
def get(url):
    with urllib.request.urlopen(url, timeout=60) as r: return json.loads(r.read())
def wait_finished(cid, token, tries=18):
    st = None
    for _ in range(tries):
        time.sleep(10)
        try: st = get(f"{API}/{cid}?fields=status_code&access_token={token}").get("status_code")
        except Exception: continue
        if st in ("FINISHED","ERROR","EXPIRED"): break
    return st
token = next(l.strip() for l in open(sys.argv[1]) if l.strip())
r = post(f"{API}/{IG_ID}/media", {"media_type": "STORIES", "video_url": sys.argv[2]}, token)
if "id" not in r:
    print("STORY PUBLISH FAILED:", json.dumps(r)[:300]); sys.exit(1)
st = wait_finished(r["id"], token)
if st != "FINISHED":
    print("STORY PUBLISH FAILED: status", st); sys.exit(1)
p = post(f"{API}/{IG_ID}/media_publish", {"creation_id": r["id"]}, token)
if "id" not in p:
    print("STORY PUBLISH FAILED:", json.dumps(p)[:300]); sys.exit(1)
print("INSTAGRAM STORY OK:", p["id"])
