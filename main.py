from typing import Any
import feedparser
from flask import Flask, send_from_directory
from werkzeug.utils import secure_filename


app: Flask = Flask(__name__)


@app.route("/<path:rss_url>")
def rewrite_rss(rss_url: str) -> str:
    """
    Given an rss url, rewrite the urls to pipe them through archive.md.
    """
    parsed = feedparser.parse(rss_url)
    for entry in parsed.entries:
        print(entry.link)
        entry.link = replace_link(entry.link)
    return str(parsed)


@app.route("/rail/<path:filename>")
def serve_rail(filename: str = "") -> Any:
    """
    Serve files from the 'rail' directory.
    """
    if not filename:
        filename = "index.html"
    filename = secure_filename(filename)
    return send_from_directory("rail", filename)


def replace_link(link: str) -> str:
    """
    Given a link, replace it with the archive.md version of it.
    Example:
    https://example.com/content
    becomes
    https://archive.ph/?run=1&url=https://example.com/content
    """
    return f"https://archive.ph/?run=1&url={link}"

if __name__ == "__main__":
    app.run(host='0.0.0.0')