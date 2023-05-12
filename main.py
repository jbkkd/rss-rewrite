import feedparser
from flask import Flask


app = Flask(__name__)


@app.route("/<path:rss_url>")
def rewrite_rss(rss_url):
    """
    Given an rss url, rewrite the urls to pipe them through archive.md.
    """
    parsed = feedparser.parse(rss_url)
    for entry in parsed.entries:
        print(entry.link)
        entry.link = replace_link(entry.link)
    return str(parsed)


def replace_link(link):
    """
    Given a link, replace it with the archive.md version of it.
    Example:
    https://example.com/content
    becomes
    https://archive.ph/?run=1&url=https://example.com/content
    """
    return f"https://archive.ph/?run=1&url={link}"
