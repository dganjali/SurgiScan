"""
Medical Researcher Agent
Searches medical literature and extracts crash cart tools required for emergency procedures.
"""

import os
import re
import json
import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
from dotenv import load_dotenv

from crash_cart_tools import get_all_tools, match_tool, get_tools_by_category

# Load environment variables
load_dotenv()

class MedicalResearcherAgent:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.crash_cart_tools = get_all_tools()
        
    def search_medical_literature(self, procedure: str) -> List[Dict]:
        """
        Search for medical literature about the procedure
        """
        # For demo purposes, we'll use predefined medical content
        # In a real implementation, this would search PubMed, NIH, etc.
        
        medical_content = {
            "Code Blue": [
                {
                    'source': 'AHA Guidelines',
                    'content': 'During a Code Blue emergency, the following equipment is essential: Epinephrine 1mg/10ml for cardiac arrest, Defibrillator with pads for shock delivery, Laryngoscope with blades for intubation, Endotracheal tubes in various sizes, Ambu bag for ventilation, IV catheters and syringes for medication administration.',
                    'url': None
                },
                {
                    'source': 'ACLS Protocol',
                    'content': 'Standard ACLS equipment includes: Atropine 1mg/10ml, Amiodarone 150mg/3ml, Calcium Chloride 10%, Sodium Bicarbonate 8.4%, Magnesium Sulfate 2g/10ml, ECG leads, Blood pressure cuff, Pulse oximeter.',
                    'url': None
                }
            ],
            "Trauma Alert": [
                {
                    'source': 'Trauma Guidelines',
                    'content': 'Trauma resuscitation requires: Tourniquet, Sterile gauze, Bandages, Scalpel, Suture kit, Chest tube kit, Foley catheter, NG tube, Cervical collar, Backboard.',
                    'url': None
                }
            ],
            "Respiratory Distress": [
                {
                    'source': 'Respiratory Protocol',
                    'content': 'For respiratory emergencies: Nasopharyngeal airway, Oropharyngeal airway, Oxygen tubing, Face mask, Nasal cannula, End-tidal CO2 detector, Capnography monitor.',
                    'url': None
                }
            ]
        }
        
        return medical_content.get(procedure, [])
    
    def extract_equipment_mentions(self, content: str) -> List[str]:
        """
        Extract equipment and tool mentions from text content
        """
        equipment_keywords = [
            'equipment', 'tool', 'device', 'instrument', 'supply', 'medication',
            'syringe', 'needle', 'catheter', 'tube', 'mask', 'bag', 'monitor',
            'defibrillator', 'laryngoscope', 'endotracheal', 'ambu', 'gloves',
            'gauze', 'tape', 'tourniquet', 'stethoscope', 'scalpel', 'suture'
        ]
        
        # Split content into sentences
        sentences = re.split(r'[.!?]+', content)
        equipment_mentions = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check for equipment keywords
            for keyword in equipment_keywords:
                if keyword in sentence_lower:
                    # Extract the phrase containing the keyword
                    words = sentence.split()
                    for i, word in enumerate(words):
                        if keyword in word.lower():
                            # Get surrounding context
                            start = max(0, i-3)
                            end = min(len(words), i+4)
                            phrase = ' '.join(words[start:end])
                            equipment_mentions.append(phrase.strip())
                            break
        
        return list(set(equipment_mentions))
    
    def match_against_crash_cart(self, equipment_mentions: List[str]) -> List[str]:
        """
        Match extracted equipment mentions against crash cart tools
        """
        matched_tools = []
        
        for mention in equipment_mentions:
            matched_tool = match_tool(mention)
            if matched_tool and matched_tool not in matched_tools:
                matched_tools.append(matched_tool)
        
        return matched_tools
    
    def get_procedure_tools(self, procedure: str) -> Dict:
        """
        Main method to get crash cart tools for a procedure
        """
        print(f"🔍 Searching medical literature for '{procedure}'...")
        
        # Search medical literature
        literature_results = self.search_medical_literature(procedure)
        
        print(f"📚 Found {len(literature_results)} literature sources")
        
        # Extract equipment mentions
        all_equipment_mentions = []
        for result in literature_results:
            mentions = self.extract_equipment_mentions(result['content'])
            all_equipment_mentions.extend(mentions)
        
        print(f"🔧 Extracted {len(all_equipment_mentions)} equipment mentions")
        
        # Match against crash cart tools
        matched_tools = self.match_against_crash_cart(all_equipment_mentions)
        
        print(f"✅ Matched {len(matched_tools)} crash cart tools")
        
        # Categorize tools
        categorized_tools = {}
        for tool in matched_tools:
            for category, tools in get_tools_by_category.__self__.CRASH_CART_TOOLS.items():
                if tool in tools:
                    if category not in categorized_tools:
                        categorized_tools[category] = []
                    categorized_tools[category].append(tool)
                    break
        
        return {
            'procedure': procedure,
            'total_tools': len(matched_tools),
            'tools': matched_tools,
            'categorized_tools': categorized_tools,
            'sources_searched': len(literature_results),
            'equipment_mentions_found': len(all_equipment_mentions)
        }

# Example usage and testing
if __name__ == "__main__":
    agent = MedicalResearcherAgent()
    
    # Test with Code Blue procedure
    result = agent.get_procedure_tools("Code Blue")
    
    print("\n" + "="*50)
    print("MEDICAL RESEARCHER AGENT RESULTS")
    print("="*50)
    print(f"Procedure: {result['procedure']}")
    print(f"Total tools found: {result['total_tools']}")
    print(f"Sources searched: {result['sources_searched']}")
    print(f"Equipment mentions found: {result['equipment_mentions_found']}")
    
    print("\nRequired Crash Cart Tools:")
    for tool in result['tools']:
        print(f"  • {tool}")
    
    print("\nCategorized Tools:")
    for category, tools in result['categorized_tools'].items():
        print(f"\n{category.upper()}:")
        for tool in tools:
            print(f"  • {tool}") 
