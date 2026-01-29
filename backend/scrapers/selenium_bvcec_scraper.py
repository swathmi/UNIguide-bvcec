import time, os, json, requests
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from PIL import Image
import pytesseract
from io import BytesIO

# ================= CONFIG =================
BASE_URL = "https://bvcec.edu.in/"
DATA_DIR = "data"
PDF_DIR = os.path.join(DATA_DIR, "pdfs")

TEXT_FILE = os.path.join(DATA_DIR, "website_scraped.txt")
IMAGE_FILE = os.path.join(DATA_DIR, "website_images.json")
PDF_FILE = os.path.join(DATA_DIR, "website_pdfs.json")

MAX_PAGES = 5000

visited = set()
queue = [BASE_URL]

text_chunks = []
images = []
pdfs = []

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

# ================= DRIVER =================
def create_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

driver = create_driver()

# ================= HELPERS =================
def is_internal(url):
    try:
        return "bvcec.edu.in" in urlparse(url).netloc
    except:
        return False

def clean(text):
    return " ".join(text.split())

def auto_scroll(d):
    last_height = d.execute_script("return document.body.scrollHeight")
    for _ in range(6):
        d.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        new_height = d.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def extract_text_from_image(url):
    try:
        r = requests.get(url, timeout=10)
        img = Image.open(BytesIO(r.content))
        text = pytesseract.image_to_string(img)
        return clean(text)
    except:
        return ""

# ================= SCRAPER =================
def scrape(url):
    if url in visited or len(visited) >= MAX_PAGES:
        return

    visited.add(url)
    print("🔍 Scraping:", url)

    try:
        driver.get(url)
        time.sleep(2)
        auto_scroll(driver)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # ---------- TEXT (STRUCTURED) ----------
        for tag in soup.find_all(["h1","h2","h3","p","li"]):
            txt = clean(tag.get_text())
            if len(txt) > 50:
                text_chunks.append(f"[SOURCE: {url}] {txt}")

        # ---------- IMAGES + OCR ----------
        for img in soup.find_all("img"):
            src = img.get("src")
            alt = clean(img.get("alt",""))

            if not src:
                continue

            full = urljoin(BASE_URL, src)
            if not is_internal(full):
                continue

            ocr_text = extract_text_from_image(full)

            images.append({
                "page": url,
                "url": full,
                "alt": alt,
                "ocr_text": ocr_text,
                "description": alt or ocr_text or "BVCEC poster / notice image"
            })

            if ocr_text and len(ocr_text) > 40:
                text_chunks.append(
                    f"[SOURCE: {url} | IMAGE: {full}] {ocr_text}"
                )

        # ---------- PDFs ----------
        for a in soup.find_all("a", href=True):
            link = urljoin(BASE_URL, a["href"])
            if link.lower().endswith(".pdf") and is_internal(link):
                name = os.path.basename(link)
                local = os.path.join(PDF_DIR, name)

                if not os.path.exists(local):
                    try:
                        pdf_data = requests.get(link, timeout=15).content
                        with open(local,"wb") as f:
                            f.write(pdf_data)
                    except:
                        pass

                pdfs.append({
                    "page": url,
                    "title": clean(a.get_text()) or name,
                    "url": link,
                    "local_path": local
                })

        # ---------- LINKS ----------
        for a in soup.find_all("a", href=True):
            link = urljoin(BASE_URL, a["href"])
            if is_internal(link) and link not in visited:
                queue.append(link)

    except Exception as e:
        print("⚠️ Error:", url, e)

# ================= RUN =================
while queue:
    scrape(queue.pop(0))

driver.quit()

# ================= CLEAN + SAVE =================
text_chunks = list(dict.fromkeys(text_chunks))
images = list({i["url"]: i for i in images}.values())
pdfs = list({p["url"]: p for p in pdfs}.values())

with open(TEXT_FILE,"w",encoding="utf-8") as f:
    f.write("\n\n".join(text_chunks))

with open(IMAGE_FILE,"w",encoding="utf-8") as f:
    json.dump(images,f,indent=2,ensure_ascii=False)

with open(PDF_FILE,"w",encoding="utf-8") as f:
    json.dump(pdfs,f,indent=2,ensure_ascii=False)

print("✅ FULL WEBSITE + IMAGES + OCR + PDFs INDEXED")
print("📄 Text  :", TEXT_FILE)
print("🖼 Images:", IMAGE_FILE)
print("📑 PDFs :", PDF_FILE)
