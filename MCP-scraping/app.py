"""
Medical Researcher Assistant - Web Application
Streamlit app for testing the crash cart tool identification system.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import time

from tool_requirement_agent import ToolRequirementAgent
from crash_cart_tools import get_all_tools, get_categories

# Page configuration
st.set_page_config(
    page_title="Medical Researcher Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize the agent
@st.cache_resource
def get_agent():
    return ToolRequirementAgent()

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .procedure-input {
        background-color: #ffffff;
        border: 2px solid #1f77b4;
        border-radius: 0.5rem;
        padding: 1rem;
    }
    .results-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .tool-item {
        background-color: #e3f2fd;
        padding: 0.5rem;
        margin: 0.25rem 0;
        border-radius: 0.25rem;
        border-left: 3px solid #2196f3;
    }
    .category-header {
        font-weight: bold;
        color: #1976d2;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Medical Researcher Assistant</h1>', unsafe_allow_html=True)
    st.markdown("### Identify Crash Cart Tools for Emergency Procedures")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Procedure input
        st.subheader("Emergency Procedure")
        procedure = st.text_input(
            "Enter procedure name:",
            value="Code Blue",
            placeholder="e.g., Code Blue, Trauma Alert, Cardiac Arrest"
        )
        
        # Options
        st.subheader("Analysis Options")
        use_llm = st.checkbox("Use LLM Analysis", value=True, help="Enable OpenAI/Claude analysis for better results")
        show_process = st.checkbox("Show Real-time Process", value=True, help="Display step-by-step analysis")
        
        # Database info
        st.subheader("📊 Database Statistics")
        agent = get_agent()
        stats = agent.get_statistics()
        
        st.metric("Total Tools", stats['total_tools'])
        st.metric("Categories", stats['categories'])
        
        # Category breakdown
        st.subheader("Tool Categories")
        for category, count in stats['tools_per_category'].items():
            st.metric(category.title(), count)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Analysis")
        
        if st.button("🔍 Analyze Procedure", type="primary", use_container_width=True):
            if procedure:
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Analysis steps
                steps = [
                    "Searching medical literature...",
                    "Web scraping additional sources...",
                    "Extracting equipment mentions...",
                    "LLM analysis..." if use_llm else "Skipping LLM analysis...",
                    "Matching against crash cart tools...",
                    "Validating equipment list..." if use_llm else "Finalizing results...",
                    "Categorizing tools...",
                    "Complete!"
                ]
                
                try:
                    # Run analysis with progress updates
                    for i, step in enumerate(steps):
                        if show_process:
                            status_text.text(step)
                        progress_bar.progress((i + 1) / len(steps))
                        time.sleep(0.5)  # Simulate processing time
                    
                    # Get results
                    result = agent.get_procedure_tools(procedure, use_llm)
                    
                    # Store results in session state
                    st.session_state['analysis_result'] = result
                    st.session_state['analysis_complete'] = True
                    
                    status_text.text("✅ Analysis complete!")
                    progress_bar.progress(1.0)
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.session_state['analysis_complete'] = False
    
    with col2:
        st.subheader("📈 Quick Stats")
        
        if 'analysis_complete' in st.session_state and st.session_state['analysis_complete']:
            result = st.session_state['analysis_result']
            
            # Metrics
            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Tools Found", result['total_tools_found'])
                st.metric("Processing Time", f"{result['processing_time_seconds']:.1f}s")
            
            with col_b:
                st.metric("Sources Analyzed", result['sources_analyzed'])
                st.metric("Confidence Score", f"{result['confidence_score']:.2f}")
        
        else:
            st.info("Run analysis to see statistics")
    
    # Results section
    if 'analysis_complete' in st.session_state and st.session_state['analysis_complete']:
        result = st.session_state['analysis_result']
        
        st.markdown("---")
        st.subheader("📋 Analysis Results")
        
        # Results overview
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Procedure", result['procedure'])
        with col2:
            st.metric("Total Tools", result['total_tools_found'])
        with col3:
            st.metric("Confidence", f"{result['confidence_score']:.2f}")
        with col4:
            st.metric("LLM Used", "Yes" if result['llm_used'] else "No")
        
        # Detailed results
        tabs = st.tabs(["📋 All Tools", "📂 By Category", "📊 Visualizations", "📄 Export"])
        
        with tabs[0]:
            st.subheader("Required Crash Cart Tools")
            if result['tools']:
                for tool in result['tools']:
                    st.markdown(f'<div class="tool-item">• {tool}</div>', unsafe_allow_html=True)
            else:
                st.warning("No tools found for this procedure")
        
        with tabs[1]:
            st.subheader("Tools by Category")
            for category, tools in result['categorized_tools'].items():
                if tools:
                    st.markdown(f'<div class="category-header">{category.upper()}</div>', unsafe_allow_html=True)
                    for tool in tools:
                        st.markdown(f'<div class="tool-item">• {tool}</div>', unsafe_allow_html=True)
        
        with tabs[2]:
            st.subheader("Data Visualizations")
            
            # Category distribution
            if result['categorized_tools']:
                category_data = []
                for category, tools in result['categorized_tools'].items():
                    if tools:
                        category_data.append({
                            'Category': category.title(),
                            'Count': len(tools)
                        })
                
                if category_data:
                    df = pd.DataFrame(category_data)
                    fig = px.bar(df, x='Category', y='Count', 
                               title="Tools by Category",
                               color='Count',
                               color_continuous_scale='Blues')
                    st.plotly_chart(fig, use_container_width=True)
                
                # Confidence gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=result['confidence_score'] * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Confidence Score"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 75], 'color': "yellow"},
                            {'range': [75, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
        
        with tabs[3]:
            st.subheader("Export Results")
            
            # JSON export
            json_str = json.dumps(result, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_str,
                file_name=f"crash_cart_tools_{result['procedure'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
            
            # CSV export for tools
            if result['tools']:
                tools_df = pd.DataFrame(result['tools'], columns=['Tool'])
                csv = tools_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Tools CSV",
                    data=csv,
                    file_name=f"tools_{result['procedure'].replace(' ', '_')}.csv",
                    mime="text/csv"
                )
            
            # Display raw JSON
            with st.expander("View Raw JSON"):
                st.json(result)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🏥 Medical Researcher Assistant | Built for TerraHacks 2025</p>
        <p>Identifies crash cart tools for emergency procedures using medical literature analysis</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
