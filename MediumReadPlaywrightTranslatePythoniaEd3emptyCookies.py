import requests

RAILWAY_URL = "https://web-production-87e15.up.railway.app"
ARTICLE_URL = "https://medium.com/predict/ukraine-destroys-su-30-medvedev-issues-a-serious-nuclear-threat-ukraine-update-5-4-2025-8d54c38fe00c"

# Paste your real Medium cookie values here — private on your device
UID_COOKIE = "<YOUR_UID_COOKIE"
SID_COOKIE = "<YOUR_SID_COOKIE>"
XSRF_COOKIE = "<YOUR_XSRF_COOKIE>"

def extract_article_text(url, cookies):
    response = requests.post(f"{RAILWAY_URL}/extract", json={
        "url": url,
        "cookies": {
            "uid": cookies["uid"],
            "sid": cookies["sid"],
            "xsrf": cookies["xsrf"]
        }
    })
    if response.status_code == 200 and "text" in response.json():
        return response.json()["text"]
    else:
        raise Exception("Extraction failed: " + str(response.text))

def translate_to_french(text):
    response = requests.post(f"{RAILWAY_URL}/translate", json={"text": text})
    if response.status_code == 200 and "translated" in response.json():
        return response.json()["translated"]
    else:
        raise Exception("Translation failed: " + str(response.text))

def save_to_file(filename, content):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

def generate_exec_summary(text, sentence_count=3):
    response = requests.post(f"{RAILWAY_URL}/summarize", json={"text": text})
    if response.status_code == 200 and "summarized" in response.json():
        return response.json()["summarized"]
    else:
        raise Exception("Summarize failed: " + str(response.text))


if __name__ == "__main__":
    ARTICLE_URL = input("Enter Medium article URL: ").strip()
    if not ARTICLE_URL.startswith("http"):
        raise ValueError("Invalid URL. Must start with http or https.")
    
    try:
        print("[INFO] Extracting article text...")
        cookies = {
            "uid": UID_COOKIE,
            "sid": SID_COOKIE,
            "xsrf": XSRF_COOKIE
        }
        english_text = extract_article_text(ARTICLE_URL, cookies)
        save_to_file("medium_article_en.txt", english_text)
        print("[INFO] Saved English version.")

        print("[INFO] Translating to French...")
        french_text = translate_to_french(english_text)
        print(french_text)
        save_to_file("medium_article_fr.txt", french_text)
        print("[SUCCESS] Saved French version.")

        print("[INFO] English text Exec Summary...")
        summary_en = generate_exec_summary(english_text, sentence_count=3)
        print(summary_en)

        print("[INFO] Résumé du texte en Français...")
        print(translate_to_french(summary_en))


    except Exception as e:
        print("[ERROR]", str(e))
