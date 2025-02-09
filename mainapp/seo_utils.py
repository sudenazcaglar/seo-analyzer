import requests
from bs4 import BeautifulSoup


def fetch_html(url):
    """Verilen URL'nin HTML içeriğini getirir."""
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status() # HTTP hata kodlarını kontrol et.
        return response.text
    except requests.exceptions.RequestException as e:
        return None
    
def analyze_seo(url):
    """Verilen URL'nin temel SEO analizini yapar."""
    html_content = fetch_html(url)
    if not html_content:
        return {"error": "URL alınamadı veya geçersiz."}
    
    soup = BeautifulSoup(html_content, "html.parser")

    # Başlık (Title) Analizi
    title = soup.title.string.strip() if soup.title and soup.title.string else "Başlık bulunamadı."

    # Meta Description Analizi
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_description["content"] if meta_description else "Meta açıklama bulunamadı."

    # H1 Etiketleri Analizi
    h1_tags = [h1.get_text(strip=True) for h1 in soup.find_all("h1")]

    # Kelime Sayısı
    words = soup.get_text().split()
    word_count = len(words)

    # Link Analizi (İç ve Dış Bağlantılar)
    links = [a['href'] for a in soup.find_all("a", href=True)]
    internal_links = [link for link in links if link.startswith("/") or url in link]
    external_links = [link for link in links if not link.startswith("/") and url not in link]

    return {
        "title": title,
        "meta_description": meta_description,
        "h1_tags": h1_tags,
        "word_count": word_count,
        "internal_links": len(internal_links),
        "external_links": len(external_links),
    }
