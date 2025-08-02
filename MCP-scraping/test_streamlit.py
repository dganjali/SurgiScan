"""
Test script for the Streamlit app functionality
"""

from streamlit_app import MedicalResearcherApp

def test_app():
    """Test the MedicalResearcherApp functionality"""
    print("🧪 Testing MedicalResearcherApp...")
    
    app = MedicalResearcherApp()
    
    # Test procedures
    test_procedures = ["Code Blue", "Trauma Alert", "Respiratory Distress"]
    
    for procedure in test_procedures:
        print(f"\n🔍 Testing procedure: {procedure}")
        
        try:
            result = app.analyze_procedure(procedure)
            
            print(f"✅ Found {result['total_tools_found']} tools")
            print(f"⏱️  Processing time: {result['processing_time_seconds']:.2f}s")
            print(f"🎯 Confidence: {result['confidence_score']:.2f}")
            print(f"📚 Sources analyzed: {result['sources_analyzed']}")
            print(f"🔧 Equipment mentions: {result['equipment_mentions_found']}")
            
            if result['tools']:
                print("📋 Sample tools:")
                for tool in result['tools'][:3]:  # Show first 3
                    print(f"  • {tool}")
            
        except Exception as e:
            print(f"❌ Error testing {procedure}: {e}")
    
    print("\n✅ All tests completed!")

if __name__ == "__main__":
    test_app() 
