from typing import Any
import json
from dicttoxml import dicttoxml
from flask import Flask, Response, send_from_directory
from werkzeug.utils import secure_filename
import requests


app: Flask = Flask(__name__)


import xml.etree.ElementTree as ET

@app.route("/<path:rss_url>")
def rewrite_rss(rss_url: str) -> Response:
    """
    Given an rss url, rewrite the urls to pipe them through archive.md.
    """
    rss_feed = requests.get(rss_url)
    root = ET.fromstring(rss_feed.content)
    for link in root.iter('link'):
        link.text = replace_link(link.text)
    modified_xml = ET.tostring(root, encoding='unicode')
    return Response(modified_xml, mimetype="application/xml")


@app.route("/rail/<path:filename>")
def serve_rail(filename: str = "") -> Any:
    """
    Serve files from the 'rail' directory.
    """
    if not filename:
        filename = "index.html"
    filename = secure_filename(filename)
    return send_from_directory("rail", filename)


def replace_link(link: str | None) -> str:
    """
    Given a link, replace it with the archive.md version of it.
    Example:
    https://example.com/content
    becomes
    https://archive.ph/?run=1&url=https://example.com/content
    """
    if not link:
        return ""
    return f"https://archive.ph/?run=1&url={link}"


if __name__ == "__main__":
    app.run(host='0.0.0.0')