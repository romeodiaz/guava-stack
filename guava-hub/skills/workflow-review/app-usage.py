#!/usr/bin/env python3
"""Web app usage for the workflow review: domain totals from local browser history.

Reads Chrome, Edge, Brave, Arc and Firefox history on this computer (Mac or Windows),
last 30 days by default, and prints only domains: visits, days used and estimated
active hours. No URLs, page titles or search terms leave this script.

    python3 app-usage.py            # top 25 domains, last 30 days
    python3 app-usage.py --days 14 --top 40
    python3 app-usage.py --self-test
"""
import argparse, glob, os, shutil, sqlite3, sys, tempfile, time
from urllib.parse import urlsplit

CHROME_EPOCH = 11644473600  # seconds from 1601 to 1970
GAP_CAP_MIN = 5  # a visit counts as active until the next one, up to 5 minutes

def history_files():
    home = os.path.expanduser("~")
    if sys.platform == "darwin":
        base = os.path.join(home, "Library", "Application Support")
        chromium = ["Google/Chrome", "Microsoft Edge", "BraveSoftware/Brave-Browser", "Arc/User Data"]
        firefox = os.path.join(base, "Firefox", "Profiles", "*", "places.sqlite")
    else:
        base = os.environ.get("LOCALAPPDATA", "")
        chromium = ["Google/Chrome/User Data", "Microsoft/Edge/User Data", "BraveSoftware/Brave-Browser/User Data"]
        firefox = os.path.join(os.environ.get("APPDATA", ""), "Mozilla", "Firefox", "Profiles", "*", "places.sqlite")
    files = [("chromium", f) for c in chromium for f in glob.glob(os.path.join(base, c, "*", "History"))]
    return files + [("firefox", f) for f in glob.glob(firefox)]

def visits(kind, path, since):
    """(unix seconds, url) for each visit since `since`, read from a copy since browsers lock the file."""
    tmp = tempfile.mkdtemp()
    db = None
    try:
        copy = os.path.join(tmp, "h.db")
        shutil.copyfile(path, copy)
        if os.path.exists(path + "-wal"):  # Firefox keeps recent visits in its write-ahead log
            shutil.copyfile(path + "-wal", copy + "-wal")
        db = sqlite3.connect(copy)
        if kind == "chromium":
            q = "SELECT v.visit_time/1e6 - ?, u.url FROM visits v JOIN urls u ON u.id = v.url WHERE v.visit_time > ?"
            rows = db.execute(q, (CHROME_EPOCH, (since + CHROME_EPOCH) * 1e6)).fetchall()
        else:
            q = "SELECT v.visit_date/1e6, p.url FROM moz_historyvisits v JOIN moz_places p ON p.id = v.place_id WHERE v.visit_date > ?"
            rows = db.execute(q, (since * 1e6,)).fetchall()
        return rows
    except (OSError, sqlite3.Error) as e:
        print(f"skipped {path}: {e}", file=sys.stderr)
        return []
    finally:
        if db:
            db.close()
        shutil.rmtree(tmp, ignore_errors=True)

def app(url):
    if not url.startswith("http"):
        return None
    try:
        host = (urlsplit(url).hostname or "").lower()
    except ValueError:
        return None
    parts = host.split(".")
    if len(parts) < 2 or host == "localhost" or host.replace(".", "").isdigit():
        return None
    if host.endswith(".google.com"):  # one domain, many apps: keep Gmail, Docs, Drive, Calendar apart
        return ".".join(parts[-3:])
    two_level = len(parts) > 2 and parts[-2] in ("co", "com", "org", "net", "gov", "ac")
    return ".".join(parts[-3:] if two_level else parts[-2:])

def totals(rows):
    """rows: (unix seconds, url) from every browser. Returns {domain: [visits, days, hours]}."""
    rows = sorted(rows)
    out = {}
    for i, (t, url) in enumerate(rows):
        d = app(url)
        if not d:
            continue
        gap = (rows[i + 1][0] - t) / 60 if i + 1 < len(rows) else 0
        r = out.setdefault(d, [0, set(), 0.0])
        r[0] += 1
        r[1].add(int(t // 86400))
        r[2] += min(gap, GAP_CAP_MIN) / 60
    return {d: [n, len(days), h] for d, (n, days, h) in out.items()}

def self_test():
    now = time.time()
    tmp = tempfile.mkdtemp()
    c = os.path.join(tmp, "History")
    db = sqlite3.connect(c)
    db.executescript("CREATE TABLE urls(id INTEGER PRIMARY KEY, url TEXT); CREATE TABLE visits(id INTEGER PRIMARY KEY, url INT, visit_time INT);")
    db.executemany("INSERT INTO urls VALUES (?,?)", [(1, "https://app.hubspot.com/x"), (2, "https://mail.google.com/m"), (3, "https://old.example.com/")])
    t0 = int((now - 3600 + CHROME_EPOCH) * 1e6)
    db.executemany("INSERT INTO visits(url, visit_time) VALUES (?,?)",
                   [(1, t0), (1, t0 + 60_000_000), (2, t0 + 120_000_000), (3, int((now - 90 * 86400 + CHROME_EPOCH) * 1e6))])
    db.commit(); db.close()
    f = os.path.join(tmp, "places.sqlite")
    db = sqlite3.connect(f)
    db.executescript("CREATE TABLE moz_places(id INTEGER PRIMARY KEY, url TEXT); CREATE TABLE moz_historyvisits(id INTEGER PRIMARY KEY, place_id INT, visit_date INT);")
    db.execute("INSERT INTO moz_places VALUES (1, 'https://www.bbc.co.uk/news')")
    db.execute("INSERT INTO moz_historyvisits(place_id, visit_date) VALUES (1, ?)", (int((now - 1800) * 1e6),))
    db.commit(); db.close()
    since = now - 30 * 86400
    t = totals(visits("chromium", c, since) + visits("firefox", f, since))
    assert set(t) == {"hubspot.com", "mail.google.com", "bbc.co.uk"}, t  # the 90-day-old visit is out
    assert t["hubspot.com"][0] == 2 and abs(t["hubspot.com"][2] - 2 / 60) < 1e-6, t  # two 1-minute gaps
    assert app("file:///x") is None and app("http://localhost:3000") is None
    assert app("http://[::1") is None and app("http://192.168.1.1/") is None
    assert app("https://a.b.docs.google.com/") == "docs.google.com"
    shutil.rmtree(tmp)
    print("self-test passed")

def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--days", type=int, default=30)
    p.add_argument("--top", type=int, default=25)
    p.add_argument("--self-test", action="store_true")
    a = p.parse_args()
    if a.self_test:
        return self_test()
    files = history_files()
    rows = [r for kind, path in files for r in visits(kind, path, time.time() - a.days * 86400)]
    t = totals(rows)
    print(f"{len(files)} browser profiles, {len(rows)} visits in the last {a.days} days")
    print(f"{'domain':32} {'visits':>7} {'days':>5} {'est. hours':>11}")
    for d, (n, days, h) in sorted(t.items(), key=lambda x: -x[1][2])[: a.top]:
        print(f"{d:32} {n:7} {days:5} {h:11.1f}")

if __name__ == "__main__":
    main()
