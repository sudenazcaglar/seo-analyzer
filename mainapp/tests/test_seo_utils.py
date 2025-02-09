from unittest.mock import patch
from django.test import TestCase
from mainapp.seo_utils import analyze_seo, fetch_html


class SEOUtilsTests(TestCase):
    
    def setUp(self):
        # Testler için farklı HTML içerikleri
        self.valid_html = """
        <html>
            <head>
                <title>Valid Page Title</title>
                <meta name="description" content="Valid meta description.">
            </head>
            <body>
                <h1>Main Heading</h1>
                <h1>Secondary Heading</h1>
                <p>Some paragraph text.</p>
                <a href="/internal-link">Internal</a>
                <a href="https://external.com">External</a>
            </body>
        </html>
        """
        self.html_no_meta = """
        <html>
            <head>
                <title>No Meta Page</title>
            </head>
            <body>
                <h1>Heading Only</h1>
                <p>Simple content.</p>
            </body>
        </html>
        """
        self.empty_html = "<html></html>"
        
    @patch("mainapp.seo_utils.fetch_html")
    def test_valid_html_analysis(self, mock_fetch_html):
        """Geçerli bir HTML ile SEO analizi çalışıyor mu?"""
        mock_fetch_html.return_value = self.valid_html

        result = analyze_seo("https://example.com")
        self.assertEqual(result["title"], "Valid Page Title")
        self.assertEqual(result["meta_description"], "Valid meta description.")
        self.assertEqual(result["h1_tags"], ["Main Heading", "Secondary Heading"])
        self.assertEqual(result["word_count"], 12)
        self.assertEqual(result["internal_links"], 1)
        self.assertEqual(result["external_links"], 1)

    @patch("mainapp.seo_utils.fetch_html")
    def test_html_no_meta(self, mock_fetch_html):
        """Meta description bulunmayan bir sayfada doğru sonuç dönüyor mu?"""
        mock_fetch_html.return_value = self.html_no_meta

        result = analyze_seo("https://example.com")
        self.assertEqual(result["title"], "No Meta Page")
        self.assertEqual(result["meta_description"], "Meta açıklama bulunamadı.")  # Beklenen default mesaj
        self.assertEqual(result["h1_tags"], ["Heading Only"])
        self.assertEqual(result["word_count"], 7)

    @patch("mainapp.seo_utils.fetch_html")
    def test_empty_html(self, mock_fetch_html):
        """Boş bir HTML analiz edildiğinde sonuçlar doğru mu?"""
        mock_fetch_html.return_value = self.empty_html

        result = analyze_seo("https://example.com")
        self.assertEqual(result["title"], "Başlık bulunamadı.")
        self.assertEqual(result["meta_description"], "Meta açıklama bulunamadı.")
        self.assertEqual(result["h1_tags"], [])
        self.assertEqual(result["word_count"], 0)
        self.assertEqual(result["internal_links"], 0)
        self.assertEqual(result["external_links"], 0)

    @patch("mainapp.seo_utils.fetch_html")
    def test_fetch_html_failure(self, mock_fetch_html):
        """fetch_html başarısız olduğunda 'error' döndürüyor mu?"""
        mock_fetch_html.return_value = None  # fetch_html None döndürüyor

        result = analyze_seo("https://example.com")
        self.assertEqual(result, {"error": "URL alınamadı veya geçersiz."})