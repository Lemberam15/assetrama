#!/usr/bin/env python3
"""Instagram CAROUSEL publisher for _assetrama (Asset Rama).

Usage: python ig_carousel_publish.py TOKEN_FILE IMAGE_URLS_FILE CAPTION_FILE
- TOKEN_FILE: skill's assets/instagram_token.txt
- IMAGE_URLS_FILE: text file, one public https image URL per line (swipe order)
- CAPTION_FILE: full caption text (includes Save line before the question)

Flow: create an IMAGE container for each card (is_carousel_item=true),
wait for FINISHED, then create the CAROUSEL container with children,
wait, publish, print the permalink.

Ram's rules honored: QC before publish (all URLs must be reachable over
https and unique), loud failure with 'CAROUSEL PUBLISH FAILED' on error.
"""
import json, sys, time, urllib.request, urllib.parse, urllib.error

IG_ID = "17841405587045840"
API = "https://graph.instagram.com/v23.0"

def post(url, data, token):
    data = dict(data, access_token=token)
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        try: return json.loads(e.read())
        except Exception: return {"_http_error": e.code}

def get(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return json.loads(r.read())

def wait_finished(cid, token, tries=18):
    status = None
    for _ in range(tries):
        time.sleep(10)
        try:
            s = get(f"{API}/{cid}?fields=status_code&access_token={token}")
        except Exception:
            continue
        status = s.get("status_code")
        if status in ("FINISHED", "ERROR", "EXPIRED"):
            break
    return status

def main():
    token = next(l.strip() for l in open(sys.argv[1]) if l.strip())
    urls = [l.strip() for l in open(sys.argv[2]) if l.strip()]
    caption = open(sys.argv[3]).read().strip()

    # pre-flight QC: unique, https, non-empty
    assert urls and len(urls) == len(set(urls)), "duplicate or missing image URLs"
    for u in urls:
        assert u.startswith("https://"), f"not https: {u}"

    children = []
    for i, u in enumerate(urls, 1):
        r = post(f"{API}/{IG_ID}/media", {"image_url": u, "is_carousel_item": "true"}, token)
        if "id" not in r:
            print(f"CAROUSEL PUBLISH FAILED: container for card {i}: {json.dumps(r)[:300]}")
            sys.exit(1)
        children.append(r["id"])
        print(f"container {i}/5: {r['id']}")

    fin = []
    for i, cid in enumerate(children, 1):
        st = wait_finished(cid, token)
        print(f"container {i} status: {st}")
        if st != "FINISHED":
            print(f"CAROUSEL PUBLISH FAILED: card {i} status {st}")
            sys.exit(1)
        fin.append(cid)

    r = post(f"{API}/{IG_ID}/media",
             {"media_type": "CAROUSEL", "children": ",".join(fin), "caption": caption}, token)
    if "id" not in r:
        print(f"CAROUSEL PUBLISH FAILED: carousel container: {json.dumps(r)[:300]}")
        sys.exit(1)
    cid = r["id"]
    st = wait_finished(cid, token)
    print(f"carousel container status: {st}")
    if st != "FINISHED":
        print("CAROUSEL PUBLISH FAILED: carousel container not FINISHED")
        sys.exit(1)
    p = post(f"{API}/{IG_ID}/media_publish", {"creation_id": cid}, token)
    if "id" not in p:
        print(f"CAROUSEL PUBLISH FAILED: publish: {json.dumps(p)[:300]}")
        sys.exit(1)
    info = get(f"{API}/{p['id']}?fields=permalink&access_token={token}")
    print("CAROUSEL OK:", info.get("permalink", p["id"]))

if __name__ == "__main__":
    main()
