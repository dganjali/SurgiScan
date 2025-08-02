"""
Tool Requirement Agent
Main orchestrator that combines medical research, web scraping, and LLM analysis
to identify crash cart tools required for emergency procedures.
"""

import time
import json
from typing import List, Dict, Optional
from datetime import datetime

from medical_researcher import MedicalResearcherAgent
from web_scraper_agent import WebScrapingAgent
from llm_agent import LLMAgent
from crash_cart_tools import get_all_tools, match_tool, get_tools_by_category

class ToolRequirementAgent:
    def __init__(self):
        self.researcher = MedicalResearcherAgent()
        self.scraper = WebScrapingAgent()
        self.llm_agent = LLMAgent()
        self.crash_cart_tools = get_all_tools()
        
    def get_procedure_tools(self, procedure: str, use_llm: bool = True) -> Dict:
        """
        Main method to get crash cart tools for a procedure
        """
        print(f"🚀 Starting analysis for procedure: {procedure}")
        start_time = time.time()
        
        # Step 1: Search medical literature
        print("📚 Step 1: Searching medical literature...")
        literature_results = self.researcher.search_medical_literature(procedure)
        
        # Step 2: Web scraping for additional sources
        print("🌐 Step 2: Web scraping additional sources...")
        scraped_results = self.scraper.search_and_scrape(f"{procedure} emergency equipment")
        
        # Step 3: Extract equipment mentions from all sources
        print("🔧 Step 3: Extracting equipment mentions...")
        all_equipment_mentions = []
        
        # From literature results
        for result in literature_results:
            mentions = self.researcher.extract_equipment_mentions(result['content'])
            all_equipment_mentions.extend(mentions)
        
        # From scraped results
        for result in scraped_results:
            all_equipment_mentions.extend(result['equipment_mentions'])
        
        # Step 4: LLM analysis if enabled
        if use_llm:
            print("🤖 Step 4: LLM analysis...")
            combined_content = self._combine_content(literature_results, scraped_results)
            llm_result = self.llm_agent.analyze_medical_content(combined_content, procedure)
            llm_equipment = llm_result.get('equipment', [])
            all_equipment_mentions.extend(llm_equipment)
        
        # Step 5: Match against crash cart tools
        print("✅ Step 5: Matching against crash cart tools...")
        matched_tools = self.researcher.match_against_crash_cart(all_equipment_mentions)
        
        # Step 6: Validate and improve list
        if use_llm:
            print("🔍 Step 6: Validating equipment list...")
            validation_result = self.llm_agent.validate_equipment_list(matched_tools)
            validated_tools = validation_result.get('equipment', matched_tools)
        else:
            validated_tools = matched_tools
        
        # Step 7: Categorize tools
        print("📂 Step 7: Categorizing tools...")
        categorized_tools = self._categorize_tools(validated_tools)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Compile results
        result = {
            'procedure': procedure,
            'timestamp': datetime.now().isoformat(),
            'processing_time_seconds': processing_time,
            'total_tools_found': len(validated_tools),
            'tools': validated_tools,
            'categorized_tools': categorized_tools,
            'sources_analyzed': len(literature_results) + len(scraped_results),
            'equipment_mentions_found': len(all_equipment_mentions),
            'llm_used': use_llm,
            'confidence_score': self._calculate_confidence_score(validated_tools, all_equipment_mentions)
        }
        
        print(f"✅ Analysis complete! Found {len(validated_tools)} tools in {processing_time:.2f} seconds")
        
        return result
    
    def _combine_content(self, literature_results: List[Dict], scraped_results: List[Dict]) -> str:
        """
        Combine content from all sources for LLM analysis
        """
        combined = []
        
        for result in literature_results:
            combined.append(result['content'][:1000])  # Limit each source
        
        for result in scraped_results:
            combined.append(result['content'][:1000])
        
        return " ".join(combined)
    
    def _categorize_tools(self, tools: List[str]) -> Dict:
        """
        Categorize tools by type
        """
        categories = {
            'medications': [],
            'airway': [],
            'vascular': [],
            'monitoring': [],
            'surgical': [],
            'emergency': []
        }
        
        for tool in tools:
            tool_lower = tool.lower()
            
            # Medications
            if any(med in tool_lower for med in ['epinephrine', 'atropine', 'amiodarone', 'lidocaine', 'dopamine', 'vasopressin', 'calcium', 'sodium', 'magnesium', 'adenosine', 'nitroglycerin', 'furosemide', 'morphine', 'ketamine', 'succinylcholine', 'rocuronium', 'midazolam', 'propofol', 'dexamethasone']):
                categories['medications'].append(tool)
            
            # Airway
            elif any(airway in tool_lower for airway in ['laryngoscope', 'endotracheal', 'ambu', 'airway', 'nasopharyngeal', 'oropharyngeal', 'cricothyrotomy', 'bougie', 'co2', 'pulse oximeter', 'oxygen', 'mask', 'cannula']):
                categories['airway'].append(tool)
            
            # Vascular
            elif any(vasc in tool_lower for vasc in ['catheter', 'syringe', 'needle', 'iv', 'tubing', 'tourniquet', 'tegaderm', 'central line', 'io', 'heparin']):
                categories['vascular'].append(tool)
            
            # Monitoring
            elif any(mon in tool_lower for mon in ['defibrillator', 'ecg', 'ekg', 'monitor', 'stethoscope', 'thermometer', 'glucometer', 'capnography', 'blood gas', 'bp cuff']):
                categories['monitoring'].append(tool)
            
            # Surgical
            elif any(surg in tool_lower for surg in ['scalpel', 'suture', 'surgical', 'chest tube', 'thoracotomy', 'foley', 'ng tube', 'gloves', 'gauze', 'tape', 'bandages']):
                categories['surgical'].append(tool)
            
            # Emergency
            else:
                categories['emergency'].append(tool)
        
        return categories
    
    def _calculate_confidence_score(self, tools: List[str], mentions: List[str]) -> float:
        """
        Calculate confidence score based on various factors
        """
        if not tools:
            return 0.0
        
        # Factor 1: Number of tools found
        tool_score = min(len(tools) / 20.0, 1.0)  # Normalize to 0-1
        
        # Factor 2: Number of mentions found
        mention_score = min(len(mentions) / 50.0, 1.0)
        
        # Factor 3: Coverage of critical categories
        categories = self._categorize_tools(tools)
        critical_categories = ['medications', 'airway', 'monitoring']
        category_score = sum(1 for cat in critical_categories if categories[cat]) / len(critical_categories)
        
        # Weighted average
        confidence = (tool_score * 0.4 + mention_score * 0.3 + category_score * 0.3)
        
        return round(confidence, 2)
    
    def get_statistics(self) -> Dict:
        """
        Get statistics about the crash cart tools database
        """
        total_tools = len(self.crash_cart_tools)
        categories = get_tools_by_category.__self__.CRASH_CART_TOOLS
        
        stats = {
            'total_tools': total_tools,
            'categories': len(categories),
            'tools_per_category': {}
        }
        
        for category, tools in categories.items():
            stats['tools_per_category'][category] = len(tools)
        
        return stats
    
    def export_results(self, results: Dict, filename: str = None) -> str:
        """
        Export results to JSON file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crash_cart_tools_{results['procedure'].replace(' ', '_')}_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        return filename

# Example usage and testing
if __name__ == "__main__":
    agent = ToolRequirementAgent()
    
    # Test with Code Blue procedure
    print("Testing ToolRequirementAgent with 'Code Blue' procedure...")
    result = agent.get_procedure_tools("Code Blue")
    
    print("\n" + "="*60)
    print("TOOL REQUIREMENT AGENT RESULTS")
    print("="*60)
    print(f"Procedure: {result['procedure']}")
    print(f"Processing time: {result['processing_time_seconds']:.2f} seconds")
    print(f"Total tools found: {result['total_tools_found']}")
    print(f"Sources analyzed: {result['sources_analyzed']}")
    print(f"Equipment mentions found: {result['equipment_mentions_found']}")
    print(f"Confidence score: {result['confidence_score']}")
    print(f"LLM used: {result['llm_used']}")
    
    print("\nRequired Crash Cart Tools:")
    for tool in result['tools']:
        print(f"  • {tool}")
    
    print("\nCategorized Tools:")
    for category, tools in result['categorized_tools'].items():
        if tools:
            print(f"\n{category.upper()}:")
            for tool in tools:
                print(f"  • {tool}")
    
    # Export results
    filename = agent.export_results(result)
    print(f"\nResults exported to: {filename}")
    
    # Show statistics
    stats = agent.get_statistics()
    print(f"\nDatabase Statistics:")
    print(f"Total tools in database: {stats['total_tools']}")
    print(f"Categories: {stats['categories']}")
    for category, count in stats['tools_per_category'].items():
        print(f"  {category}: {count} tools") 
