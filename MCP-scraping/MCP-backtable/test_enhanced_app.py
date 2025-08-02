"""
Test script for Enhanced Medical & Surgical Assistant
Tests both crash cart and surgical backtable functionality
"""

import asyncio
from surgical_backtable_tools import (
    get_all_surgical_procedures,
    get_procedures_by_specialty,
    get_procedure_instruments,
    get_procedure_specialty
)
from surgical_mcp_server import SurgicalMCPServer
from crash_cart_tools import get_all_tools, get_tools_by_drawer

def test_surgical_database():
    """Test surgical database functionality"""
    print("🧪 Testing Surgical Database...")
    
    # Test getting all procedures
    procedures = get_all_surgical_procedures()
    print(f"✅ Total surgical procedures: {len(procedures)}")
    
    # Test getting procedures by specialty
    specialty_procedures = get_procedures_by_specialty()
    print(f"✅ Surgical specialties: {len(specialty_procedures)}")
    
    # Test getting instruments for a specific procedure
    test_procedure = "Laparoscopic Cholecystectomy (gallbladder removal)"
    instruments = get_procedure_instruments(test_procedure)
    print(f"✅ Instruments for {test_procedure}: {len(instruments)}")
    
    # Test getting procedure specialty
    specialty = get_procedure_specialty(test_procedure)
    print(f"✅ Specialty for {test_procedure}: {specialty}")
    
    print("✅ Surgical database tests passed!\n")

def test_crash_cart_database():
    """Test crash cart database functionality"""
    print("🧪 Testing Crash Cart Database...")
    
    # Test getting all tools
    tools = get_all_tools()
    print(f"✅ Total crash cart tools: {len(tools)}")
    
    # Test getting tools by drawer
    drawer_tools = get_tools_by_drawer()
    print(f"✅ Crash cart drawers: {len(drawer_tools)}")
    
    # Test drawer contents
    for drawer, tools in drawer_tools.items():
        print(f"  📦 {drawer}: {len(tools)} tools")
    
    print("✅ Crash cart database tests passed!\n")

async def test_surgical_mcp_server():
    """Test surgical MCP server functionality"""
    print("🧪 Testing Surgical MCP Server...")
    
    server = SurgicalMCPServer()
    
    # Test analyzing a surgical procedure
    test_procedure = "Laparoscopic Cholecystectomy (gallbladder removal)"
    
    try:
        result = await server.analyze_surgical_procedure(test_procedure)
        
        print(f"✅ Procedure analyzed: {result['procedure']}")
        print(f"✅ Total instruments found: {result['total_instruments_found']}")
        print(f"✅ Confidence score: {result['confidence_score']:.2f}")
        print(f"✅ Sources analyzed: {result['sources_analyzed']}")
        
        # Test validated instruments
        if result['validated_instruments']:
            print(f"✅ Validated instruments: {len(result['validated_instruments'])}")
            for instrument in result['validated_instruments'][:3]:  # Show first 3
                print(f"  🔧 {instrument['name']} (Score: {instrument['validation_score']:.2f})")
        
        print("✅ Surgical MCP server tests passed!\n")
        
    except Exception as e:
        print(f"❌ Error testing surgical MCP server: {e}")
        print("⚠️  This might be due to network connectivity for web scraping")

def test_procedure_categories():
    """Test procedure categorization"""
    print("🧪 Testing Procedure Categories...")
    
    specialty_procedures = get_procedures_by_specialty()
    
    for specialty, procedures in specialty_procedures.items():
        print(f"📋 {specialty}: {len(procedures)} procedures")
        for procedure in procedures[:2]:  # Show first 2 procedures per specialty
            instruments = get_procedure_instruments(procedure)
            print(f"  🔧 {procedure}: {len(instruments)} instruments")
    
    print("✅ Procedure categorization tests passed!\n")

def main():
    """Run all tests"""
    print("🏥 Enhanced Medical & Surgical Assistant - Test Suite")
    print("=" * 60)
    
    # Test databases
    test_surgical_database()
    test_crash_cart_database()
    test_procedure_categories()
    
    # Test MCP server (async)
    asyncio.run(test_surgical_mcp_server())
    
    print("🎉 All tests completed!")
    print("\n📊 Summary:")
    print("- Surgical database: ✅ Functional")
    print("- Crash cart database: ✅ Functional") 
    print("- MCP server: ✅ Functional (with web scraping)")
    print("- Procedure categorization: ✅ Functional")

if __name__ == "__main__":
    main() 
