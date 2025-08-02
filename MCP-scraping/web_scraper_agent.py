"""
Web Scraping Agent
Enhanced web scraping capabilities for medical literature and guidelines.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
from typing import List, Dict, Optional
import json

class WebScrapingAgent:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def scrape_medical_guidelines(self, url: str) -> Dict:
        """
        Scrape medical guidelines from a URL
        """
        try:
            response = self.session.get(url, timeout=10)
            if response.status_code == 200:
                return self._parse_medical_content(response.text, url)
            else:
                print(f"Failed to fetch {url}: Status {response.status_code}")
                
        except Exception as e:
            print(f"Error scraping {url}: {e}")
        
        return {'url': url, 'content': '', 'equipment_mentions': []}
    
    def _parse_medical_content(self, html_content: str, url: str) -> Dict:
        """
        Parse medical content from HTML
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()
        
        # Extract text content
        text_content = soup.get_text()
        
        # Clean up text
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_content = ' '.join(chunk for chunk in chunks if chunk)
        
        # Extract equipment mentions
        equipment_mentions = self._extract_equipment_from_text(text_content)
        
        # Extract structured data if available
        structured_data = self._extract_structured_data(soup)
        
        return {
            'url': url,
            'content': text_content,
            'equipment_mentions': equipment_mentions,
            'structured_data': structured_data,
            'title': soup.title.string if soup.title else '',
            'meta_description': self._get_meta_description(soup)
        }
    
    def _extract_equipment_from_text(self, text: str) -> List[str]:
        """
        Extract equipment mentions from text content
        """
        equipment_patterns = [
            r'\b(defibrillator|AED|shock\s+box)\b',
            r'\b(laryngoscope|endotracheal\s+tube|ET\s+tube)\b',
            r'\b(ambu\s+bag|bag\s+valve\s+mask|BMV)\b',
            r'\b(syringe|needle|catheter|IV)\b',
            r'\b(epinephrine|adrenaline|atropine|amiodarone)\b',
            r'\b(gloves|gauze|tape|tourniquet)\b',
            r'\b(stethoscope|monitor|ECG|EKG)\b',
            r'\b(scalpel|suture|surgical)\b',
            r'\b(oxygen|mask|tubing)\b',
            r'\b(medication|drug|injection)\b'
        ]
        
        equipment_mentions = []
        
        for pattern in equipment_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                # Get surrounding context
                start = max(0, match.start() - 50)
                end = min(len(text), match.end() + 50)
                context = text[start:end].strip()
                equipment_mentions.append(context)
        
        return list(set(equipment_mentions))
    
    def _extract_structured_data(self, soup: BeautifulSoup) -> Dict:
        """
        Extract structured data from JSON-LD or microdata
        """
        structured_data = {}
        
        # Look for JSON-LD structured data
        json_ld_scripts = soup.find_all('script', type='application/ld+json')
        for script in json_ld_scripts:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    structured_data['json_ld'] = data
            except:
                continue
        
        # Look for microdata
        microdata = soup.find_all(attrs={'itemtype': True})
        if microdata:
            structured_data['microdata'] = []
            for item in microdata:
                structured_data['microdata'].append({
                    'itemtype': item.get('itemtype'),
                    'content': item.get_text().strip()
                })
        
        return structured_data
    
    def _get_meta_description(self, soup: BeautifulSoup) -> str:
        """
        Extract meta description
        """
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc:
            return meta_desc.get('content', '')
        return ''
    
    def scrape_multiple_sources(self, urls: List[str]) -> List[Dict]:
        """
        Scrape multiple medical sources
        """
        results = []
        
        for url in urls:
            print(f"🔍 Scraping: {url}")
            result = self.scrape_medical_guidelines(url)
            results.append(result)
            time.sleep(1)  # Be respectful to servers
        
        return results
    
    def search_and_scrape(self, search_query: str, max_results: int = 5) -> List[Dict]:
        """
        Search for medical content and scrape the results
        """
        # This would integrate with a search API
        # For now, we'll use some known medical guideline URLs
        medical_urls = [
            "https://www.heart.org/en/professional/guidelines-and-statements",
            "https://www.uptodate.com/contents/search",
            "https://www.medscape.com/",
            "https://www.ncbi.nlm.nih.gov/books/NBK441940/",
            "https://www.acep.org/patient-care/policy-statements/"
        ]
        
        results = []
        for url in medical_urls[:max_results]:
            try:
                result = self.scrape_medical_guidelines(url)
                if result['content'] and len(result['content']) > 100:
                    results.append(result)
            except Exception as e:
                print(f"Error scraping {url}: {e}")
        
        return results

# Example usage
if __name__ == "__main__":
    scraper = WebScrapingAgent()
    
    # Test scraping
    test_url = "https://www.heart.org/en/professional/guidelines-and-statements"
    result = scraper.scrape_medical_guidelines(test_url)
    
    print("Web Scraping Results:")
    print(f"URL: {result['url']}")
    print(f"Title: {result['title']}")
    print(f"Content length: {len(result['content'])} characters")
    print(f"Equipment mentions found: {len(result['equipment_mentions'])}")
    
    for mention in result['equipment_mentions'][:5]:  # Show first 5
        print(f"  • {mention}") 
