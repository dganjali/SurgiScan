"""
Demo Script for Medical Researcher Assistant
Shows the system in action with a Code Blue procedure.
"""

import time
from tool_requirement_agent import ToolRequirementAgent

def demo_code_blue():
    """Demo the system with Code Blue procedure"""
    print("🏥 Medical Researcher Assistant - Demo")
    print("="*50)
    print("Procedure: Code Blue (Cardiac Arrest)")
    print("="*50)
    
    # Initialize the agent
    print("🚀 Initializing system...")
    agent = ToolRequirementAgent()
    
    # Run analysis
    print("\n🔍 Starting analysis...")
    start_time = time.time()
    
    result = agent.get_procedure_tools("Code Blue", use_llm=False)  # Disable LLM for demo
    
    processing_time = time.time() - start_time
    
    # Display results
    print(f"\n✅ Analysis complete in {processing_time:.2f} seconds!")
    print(f"📊 Found {result['total_tools_found']} crash cart tools")
    print(f"📚 Analyzed {result['sources_analyzed']} medical sources")
    print(f"🔧 Extracted {result['equipment_mentions_found']} equipment mentions")
    print(f"🎯 Confidence score: {result['confidence_score']:.2f}")
    
    # Show tools by category
    print("\n📋 Required Crash Cart Tools:")
    print("-" * 40)
    
    for category, tools in result['categorized_tools'].items():
        if tools:
            print(f"\n{category.upper()}:")
            for tool in tools:
                print(f"  • {tool}")
    
    # Show all tools
    print(f"\n📋 Complete Tool List ({len(result['tools'])} items):")
    print("-" * 40)
    for i, tool in enumerate(result['tools'], 1):
        print(f"{i:2d}. {tool}")
    
    # Show statistics
    print(f"\n📈 Performance Metrics:")
    print(f"  • Processing time: {processing_time:.2f} seconds")
    print(f"  • Sources analyzed: {result['sources_analyzed']}")
    print(f"  • Equipment mentions: {result['equipment_mentions_found']}")
    print(f"  • Confidence score: {result['confidence_score']:.2f}")
    print(f"  • LLM used: {'Yes' if result['llm_used'] else 'No'}")
    
    return result

def demo_multiple_procedures():
    """Demo with multiple procedures"""
    print("\n" + "="*50)
    print("🔍 Multi-Procedure Demo")
    print("="*50)
    
    agent = ToolRequirementAgent()
    
    procedures = [
        "Code Blue",
        "Trauma Alert",
        "Respiratory Distress"
    ]
    
    results = {}
    
    for procedure in procedures:
        print(f"\n🔍 Analyzing: {procedure}")
        try:
            result = agent.get_procedure_tools(procedure, use_llm=False)
            results[procedure] = result
            
            print(f"✅ Found {result['total_tools_found']} tools")
            print(f"⏱️  Processing time: {result['processing_time_seconds']:.2f}s")
            print(f"🎯 Confidence: {result['confidence_score']:.2f}")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Compare results
    print(f"\n📊 Comparison Summary:")
    print("-" * 40)
    for procedure, result in results.items():
        print(f"{procedure:20} | {result['total_tools_found']:2d} tools | {result['confidence_score']:.2f} confidence")
    
    return results

def main():
    """Run the demo"""
    print("🎬 Starting Medical Researcher Assistant Demo")
    print("This demo shows how the system identifies crash cart tools for emergency procedures.")
    
    # Demo 1: Code Blue
    result = demo_code_blue()
    
    # Demo 2: Multiple procedures
    multi_results = demo_multiple_procedures()
    
    print("\n" + "="*50)
    print("🎉 Demo Complete!")
    print("="*50)
    print("The system successfully identified crash cart tools for emergency procedures.")
    print("This can be integrated with OpenMV cameras and SAM for real-time validation.")
    
    # Export demo results
    demo_data = {
        'code_blue': result,
        'multi_procedure': multi_results,
        'demo_timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
    }
    
    import json
    with open('demo_results.json', 'w') as f:
        json.dump(demo_data, f, indent=2)
    
    print(f"\n📄 Demo results exported to: demo_results.json")

if __name__ == "__main__":
    main() 
