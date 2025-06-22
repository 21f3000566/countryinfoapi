# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "beautifulsoup4",
#     "fastapi",
#     "requests"
# ]]
# ///
from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
from bs4 import BeautifulSoup
import traceback

@app.get("/api/outline", response_class=PlainTextResponse)
def get_outline(request: Request):
    try:
        country = request.query_params.get("country")
        if not country:
            return "# Error\n\nMissing ?country= query parameter."

        url = f"https://en.wikipedia.org/wiki/{country.replace(' ', '_')}"
        res = requests.get(url, timeout=5)
        res.raise_for_status()

        soup = BeautifulSoup(res.text, "html.parser")
        headings = soup.find_all(["h1","h2","h3","h4","h5","h6"])

        markdown = f"# {country}\n\n"
        for tag in headings:
            level = int(tag.name[1])
            text = tag.get_text(strip=True)
            if text and not text.lower().startswith("jump to"):
                markdown += f"{'#' * level} {text}\n\n"

        return markdown.strip()

    except Exception as e:
        error_text = traceback.format_exc()
        print(error_text)  # This will appear in Vercel logs
        return f"# Error\n\nAn internal exception occurred:\n\n```\n{str(e)}\n```"
