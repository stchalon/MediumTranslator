import requests
from bs4 import BeautifulSoup

def download_medium_article(url):
    """
    Fetches and extracts text from a Medium article
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X)'
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for element in soup(['script', 'style', 'nav', 'footer', 'iframe', 'img']):
            element.decompose()
        
        paragraphs = soup.find_all('p')
        if not paragraphs:
            raise Exception("No content found in article.")
        
        return '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
        
    except Exception as e:
        raise Exception(f"Failed to download article: {str(e)}")

def detect_language_google(text):
    """
    Uses Google Translate to detect language.
    """
    try:
        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "en",
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params)
        result = response.json()
        return result[2]  # Detected language code
    except Exception as e:
        print(f"Language detection failed: {e}")
        return "unknown"

def translate_to_french(text):
    """
    Translates text to French using Google's unofficial API (no key required).
    """
    try:
        lang = detect_language_google(text[:300])
        print(f"Detected language: [{lang}]")

        if lang == 'fr':
            return text

        url = "https://translate.googleapis.com/translate_a/single"
        params = {
            "client": "gtx",
            "sl": "auto",
            "tl": "fr",
            "dt": "t",
            "q": text
        }
        response = requests.get(url, params=params)
        translated = ''.join(part[0] for part in response.json()[0])
        return translated
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

if __name__ == "__main__":
    try:
        medium_url = input("Enter Medium article URL: ").strip()
        if not medium_url.startswith("http"):
            raise ValueError("Invalid URL. Must start with http or https.")
        
        print(f"\nDownloading: {medium_url}")
        article_text = download_medium_article(medium_url)
        
        print("\nTranslating to French...")
        french_text = translate_to_french(article_text)
        
        print("\n--- Translated Text ---\n")
        print(french_text[:2000] + "...")  # Preview

        save = input("\nSave to file? (y/n): ").lower()
        if save == 'y':
            filename = "translated_article.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(french_text)
            print(f"Saved to {filename}")
            
    except Exception as e:
        print(f"Error: {str(e)}")