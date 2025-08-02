"""
LLM Agent for Medical Equipment Analysis
Uses keyword-based analysis to extract equipment requirements.
"""

import os
import json
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class LLMAgent:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        
    def analyze_medical_content(self, content: str, procedure: str) -> Dict:
        """
        Analyze medical content and extract equipment requirements using keyword matching
        """
        # Use keyword-based analysis instead of LLM
        equipment_keywords = [
            'epinephrine', 'atropine', 'amiodarone', 'lidocaine', 'dopamine',
            'defibrillator', 'laryngoscope', 'endotracheal', 'ambu', 'syringe',
            'needle', 'catheter', 'gloves', 'gauze', 'tape', 'tourniquet',
            'stethoscope', 'scalpel', 'suture', 'oxygen', 'mask', 'tubing',
            'medication', 'drug', 'injection', 'monitor', 'ecg', 'ekg',
            'pulse oximeter', 'blood pressure', 'thermometer', 'glucometer'
        ]
        
        extracted_equipment = []
        content_lower = content.lower()
        
        for keyword in equipment_keywords:
            if keyword in content_lower:
                # Find the context around the keyword
                start = content_lower.find(keyword)
                end = start + len(keyword)
                
                # Get surrounding context
                context_start = max(0, start - 20)
                context_end = min(len(content), end + 20)
                context = content[context_start:context_end].strip()
                
                extracted_equipment.append(context)
        
        return {
            'equipment': list(set(extracted_equipment)),
            'source': 'keyword_analysis',
            'confidence': 'medium'
        }
    
    def validate_equipment_list(self, equipment_list: List[str]) -> Dict:
        """
        Validate and improve equipment list using keyword matching
        """
        # Simple validation - keep items that contain medical keywords
        medical_keywords = [
            'epinephrine', 'atropine', 'defibrillator', 'laryngoscope',
            'endotracheal', 'ambu', 'syringe', 'needle', 'catheter',
            'gloves', 'gauze', 'tape', 'tourniquet', 'stethoscope',
            'scalpel', 'suture', 'oxygen', 'mask', 'tubing'
        ]
        
        validated_equipment = []
        for item in equipment_list:
            item_lower = item.lower()
            if any(keyword in item_lower for keyword in medical_keywords):
                validated_equipment.append(item)
        
        return {
            'validated_equipment': validated_equipment,
            'confidence': 'medium'
        }
    
    def categorize_equipment(self, equipment_list: List[str]) -> Dict:
        """
        Categorize equipment by type
        """
        categories = {
            'medications': [],
            'airway': [],
            'vascular': [],
            'monitoring': [],
            'surgical': [],
            'emergency': []
        }
        
        for item in equipment_list:
            item_lower = item.lower()
            
            if any(med in item_lower for med in ['epinephrine', 'atropine', 'amiodarone', 'lidocaine', 'dopamine']):
                categories['medications'].append(item)
            elif any(airway in item_lower for airway in ['laryngoscope', 'endotracheal', 'ambu', 'airway']):
                categories['airway'].append(item)
            elif any(vasc in item_lower for vasc in ['catheter', 'syringe', 'needle', 'iv']):
                categories['vascular'].append(item)
            elif any(mon in item_lower for mon in ['defibrillator', 'ecg', 'monitor', 'stethoscope']):
                categories['monitoring'].append(item)
            elif any(surg in item_lower for surg in ['scalpel', 'suture', 'surgical']):
                categories['surgical'].append(item)
            else:
                categories['emergency'].append(item)
        
        return categories

# Example usage
if __name__ == "__main__":
    agent = LLMAgent()
    
    # Test content
    test_content = """
    During a Code Blue emergency, the following equipment is essential:
    - Epinephrine 1mg/10ml for cardiac arrest
    - Defibrillator with pads for shock delivery
    - Laryngoscope with blades for intubation
    - Endotracheal tubes in various sizes
    - Ambu bag for ventilation
    - IV catheters and syringes for medication administration
    """
    
    result = agent.analyze_medical_content(test_content, "Code Blue")
    print("LLM Analysis Results:")
    print(f"Equipment found: {result['equipment']}")
    print(f"Source: {result['source']}")
    print(f"Confidence: {result['confidence']}")
    
    # Test categorization
    categories = agent.categorize_equipment(result['equipment'])
    print("\nCategorized Equipment:")
    for category, items in categories.items():
        if items:
            print(f"{category}: {items}") 
