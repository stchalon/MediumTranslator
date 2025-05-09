
# Your Medium cookies (replace with your actual values)
UID_COOKIE = "<YOUR_UID_COOKIE>"
SID_COOKIE = "<YOUR_SID_COOKIE>"
XSRF_COOKIE = "<YOUR_XSRF_COOKIE>"

# The Medium article URL you want to extract text from
ARTICLE_URL = "https://medium.com/@christopherpjones/the-unflinching-intensity-of-vermeers-most-famous-painting-8df86ec6d7f9

from playwright.sync_api import sync_playwright
from deep_translator import GoogleTranslator
import re


# Max characters for translation
MAX_CHARACTERS = 3000

def format_to_markdown(text):
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
    md_lines = []

    for p in paragraphs:
        if p.isupper() and len(p.split()) < 10:
            md_lines.append(f"## {p.title()}")
        elif re.match(r"^[-•*]\s+", p):
            md_lines.append(f"- {p[2:].strip()}")
        else:
            md_lines.append(p)

    return "\n\n".join(md_lines)

def translate_text_chunked(text, target_lang="fr"):
    print("[INFO] Translating to French in chunks...")
    # Split the text into chunks of MAX_CHARACTERS
    chunks = [text[i:i + MAX_CHARACTERS] for i in range(0, len(text), MAX_CHARACTERS)]
    translated_chunks = []

    for chunk in chunks:
        translated_chunk = GoogleTranslator(source='auto', target=target_lang).translate(chunk)
        translated_chunks.append(translated_chunk)
    
    return ''.join(translated_chunks)

def extract_medium_article(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/124.0.0.0 Safari/537.36"
        )

        context.add_cookies([
            {"name": "uid", "value": UID_COOKIE, "domain": ".medium.com", "path": "/", "httpOnly": True, "secure": True},
            {"name": "sid", "value": SID_COOKIE, "domain": ".medium.com", "path": "/", "httpOnly": True, "secure": True},
            {"name": "xsrf", "value": XSRF_COOKIE, "domain": ".medium.com", "path": "/", "httpOnly": False, "secure": True}
        ])

        page = context.new_page()
        try:
            print("[INFO] Navigating to page...")
            page.goto(url, wait_until="load", timeout=60000)
            page.wait_for_selector("article", timeout=30000)

            raw_text = page.locator("article").first.inner_text()
            markdown = format_to_markdown(raw_text)

            # Translate the entire article in chunks
            markdown_fr = translate_text_chunked(markdown)
            print(markdown_fr)

            # Save both original and translated
            with open("medium_article_en.md", "w", encoding="utf-8") as f:
                f.write(markdown)
            with open("medium_article_fr.md", "w", encoding="utf-8") as f:
                f.write(markdown_fr)

            print("[SUCCESS] Saved English and French versions.")
            return markdown_fr

        except Exception as e:
            print("[ERROR] Failed to load or extract article:", str(e))
            page.screenshot(path="error_screenshot.png")
            return ""

        finally:
            browser.close()

if __name__ == "__main__":
    ARTICLE_URL = input("Enter Medium article URL: ").strip()
    if not ARTICLE_URL.startswith("http"):
        raise ValueError("Invalid URL. Must start with http or https.")
    
    extract_medium_article(ARTICLE_URL)
