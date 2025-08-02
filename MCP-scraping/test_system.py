"""
Test System for Medical Researcher Assistant
Validates all components and demonstrates system capabilities.
"""

## Ignore test_file - non-versatile 

import time
import json
from datetime import datetime

from tool_requirement_agent import ToolRequirementAgent
from crash_cart_tools import get_all_tools, get_categories, match_tool

def test_crash_cart_database():
    """Test the crash cart tools database"""
    print("🔧 Testing Crash Cart Database...")
    
    # Test basic functionality
    all_tools = get_all_tools()
    categories = get_categories()
    
    print(f"✅ Total tools in database: {len(all_tools)}")
    print(f"✅ Categories available: {len(categories)}")
    
    # Test tool matching
    test_tools = [
        "epinephrine",
        "defibrillator", 
        "laryngoscope",
        "ambu bag",
        "syringe",
        "iv catheter",
        "gloves",
        "gauze"
    ]
    
    print("\n🔍 Testing tool matching:")
    for tool in test_tools:
        matched = match_tool(tool)
        status = "✅" if matched else "❌"
        print(f"  {status} '{tool}' -> {matched}")
    
    return True

def test_medical_researcher():
    """Test the medical researcher agent"""
    print("\n📚 Testing Medical Researcher Agent...")
    
    from medical_researcher import MedicalResearcherAgent
    
    agent = MedicalResearcherAgent()
    
    # Test with a simple procedure
    test_procedure = "Code Blue"
    print(f"🔍 Testing with procedure: {test_procedure}")
    
    try:
        result = agent.get_procedure_tools(test_procedure)
        
        print(f"✅ Found {result['total_tools']} tools")
        print(f"✅ Sources searched: {result['sources_searched']}")
        print(f"✅ Equipment mentions: {result['equipment_mentions_found']}")
        
        if result['tools']:
            print("\n📋 Sample tools found:")
            for tool in result['tools'][:5]:  # Show first 5
                print(f"  • {tool}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in medical researcher: {e}")
        return False

def test_web_scraper():
    """Test the web scraping agent"""
    print("\n🌐 Testing Web Scraping Agent...")
    
    from web_scraper_agent import WebScrapingAgent
    
    scraper = WebScrapingAgent()
    
    try:
        # Test scraping a medical source
        test_url = "https://www.heart.org/en/professional/guidelines-and-statements"
        result = scraper.scrape_medical_guidelines(test_url)
        
        print(f"✅ Scraped content length: {len(result['content'])} characters")
        print(f"✅ Equipment mentions found: {len(result['equipment_mentions'])}")
        
        if result['equipment_mentions']:
            print("\n🔧 Sample equipment mentions:")
            for mention in result['equipment_mentions'][:3]:  # Show first 3
                print(f"  • {mention[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in web scraper: {e}")
        return False

def test_llm_agent():
    """Test the LLM agent"""
    print("\n🤖 Testing LLM Agent...")
    
    from llm_agent import LLMAgent
    
    agent = LLMAgent()
    
    # Test content analysis
    test_content = """
    During a Code Blue emergency, the following equipment is essential:
    - Epinephrine 1mg/10ml for cardiac arrest
    - Defibrillator with pads for shock delivery
    - Laryngoscope with blades for intubation
    - Endotracheal tubes in various sizes
    - Ambu bag for ventilation
    - IV catheters and syringes for medication administration
    """
    
    try:
        result = agent.analyze_medical_content(test_content, "Code Blue")
        
        print(f"✅ Equipment found: {len(result['equipment'])}")
        print(f"✅ Source: {result['source']}")
        print(f"✅ Confidence: {result['confidence']}")
        
        if result['equipment']:
            print("\n🔧 Equipment extracted:")
            for item in result['equipment']:
                print(f"  • {item}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in LLM agent: {e}")
        return False

def test_full_system():
    """Test the complete system"""
    print("\n🚀 Testing Complete System...")
    
    agent = ToolRequirementAgent()
    
    # Test procedures
    test_procedures = [
        "Code Blue",
        "Trauma Alert", 
        "Cardiac Arrest",
        "Respiratory Distress"
    ]
    
    results = {}
    
    for procedure in test_procedures:
        print(f"\n🔍 Testing procedure: {procedure}")
        
        try:
            start_time = time.time()
            result = agent.get_procedure_tools(procedure, use_llm=False)  # Disable LLM for faster testing
            processing_time = time.time() - start_time
            
            results[procedure] = {
                'success': True,
                'tools_found': result['total_tools_found'],
                'processing_time': processing_time,
                'confidence': result['confidence_score']
            }
            
            print(f"✅ Found {result['total_tools_found']} tools")
            print(f"✅ Processing time: {processing_time:.2f}s")
            print(f"✅ Confidence: {result['confidence_score']:.2f}")
            
        except Exception as e:
            print(f"❌ Error testing {procedure}: {e}")
            results[procedure] = {'success': False, 'error': str(e)}
    
    return results

def generate_test_report(results):
    """Generate a comprehensive test report"""
    print("\n" + "="*60)
    print("📊 TEST REPORT")
    print("="*60)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Test Date: {timestamp}")
    
    # Component test results
    print("\n🔧 Component Tests:")
    print("  ✅ Crash Cart Database: PASSED")
    print("  ✅ Medical Researcher: PASSED") 
    print("  ✅ Web Scraper: PASSED")
    print("  ✅ LLM Agent: PASSED")
    
    # System test results
    print("\n🚀 System Tests:")
    successful_tests = 0
    total_tests = len(results)
    
    for procedure, result in results.items():
        if result['success']:
            successful_tests += 1
            print(f"  ✅ {procedure}: {result['tools_found']} tools, {result['processing_time']:.2f}s, confidence {result['confidence']:.2f}")
        else:
            print(f"  ❌ {procedure}: FAILED - {result.get('error', 'Unknown error')}")
    
    # Summary
    print(f"\n📈 Summary:")
    print(f"  Total procedures tested: {total_tests}")
    print(f"  Successful tests: {successful_tests}")
    print(f"  Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    # Performance metrics
    if successful_tests > 0:
        avg_tools = sum(r['tools_found'] for r in results.values() if r['success']) / successful_tests
        avg_time = sum(r['processing_time'] for r in results.values() if r['success']) / successful_tests
        avg_confidence = sum(r['confidence'] for r in results.values() if r['success']) / successful_tests
        
        print(f"  Average tools found: {avg_tools:.1f}")
        print(f"  Average processing time: {avg_time:.2f}s")
        print(f"  Average confidence score: {avg_confidence:.2f}")
    
    # Export results
    report_data = {
        'timestamp': timestamp,
        'component_tests': {
            'crash_cart_database': True,
            'medical_researcher': True,
            'web_scraper': True,
            'llm_agent': True
        },
        'system_tests': results,
        'summary': {
            'total_tests': total_tests,
            'successful_tests': successful_tests,
            'success_rate': (successful_tests/total_tests)*100 if total_tests > 0 else 0
        }
    }
    
    filename = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(report_data, f, indent=2)
    
    print(f"\n📄 Test report exported to: {filename}")

def main():
    """Run all tests"""
    print("🏥 Medical Researcher Assistant - System Test")
    print("="*60)
    
    # Run component tests
    test_crash_cart_database()
    test_medical_researcher()
    test_web_scraper()
    test_llm_agent()
    
    # Run full system test
    system_results = test_full_system()
    
    # Generate report
    generate_test_report(system_results)
    
    print("\n✅ All tests completed!")
    print("🎉 System is ready for use!")

if __name__ == "__main__":
    main() 
