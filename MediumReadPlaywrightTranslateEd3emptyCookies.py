import requests
import sound
import requests
import tempfile

RAILWAY_URL = "https://web-production-87e15.up.railway.app"

ARTICLE_URL = "https://medium.com/predict/ukraine-destroys-su-30-medvedev-issues-a-serious-nuclear-threat-ukraine-update-5-4-2025-8d54c38fe00c"

# Paste your real Medium cookie values here — private on your device
UID_COOKIE = "<YOUR_UID>"
SID_COOKIE = "<YOUR_SID>"
XSRF_COOKIE = "<YOUR_XSRF>"

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


def play_tts_ios(text, lang="fr"):
  response = requests.post(f"{RAILWAY_URL}/tts", json={"text": text, "lang": lang})

  if response.status_code == 200:
      with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
          f.write(response.content)
          f.flush()
          sound.play_effect(f.name)
          print("Playing on iOS")
  else:
      print("Error:", response.status_code, response.text)


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

      print("\n[INFO] English text Exec Summary...")
      summary_en = generate_exec_summary(english_text, sentence_count=3)
      print(summary_en)

      print("\n[INFO] Résumé du texte en Français...")
      summary_fr=translate_to_french(summary_en)
      print(summary_fr)

      #1st option import speech (your iOS language only)
      #1st option: speech.say(summary_fr)

      #2nd option (iOS only, select your language)
      play_tts_ios(summary_en,'en')
      #play_tts_ios(summary_fr)

  except Exception as e:
      print("[ERROR]", str(e))
