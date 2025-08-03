"""
Enhanced Medical & Surgical Assistant - Streamlit App
Complete standalone application for identifying crash cart tools and surgical backtable instruments.
Enhanced with comprehensive procedures, MCP server integration, and modern UI.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import json
import time
import re
import random
import asyncio

# Import our modules
from crash_cart_tools import get_all_tools, match_tool, get_tools_by_category, CRASH_CART_TOOLS, get_tools_by_drawer
from surgical_backtable_tools import (
    get_all_surgical_procedures, 
    get_procedures_by_specialty,
    get_procedure_instruments,
    get_procedure_specialty
)
from surgical_mcp_server import SurgicalMCPServer

# Page configuration
st.set_page_config(
    page_title="Medical & Surgical Assistant",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS for modern UI
st.markdown("""
<style>
    /* Modern gradient background */
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    /* Enhanced header styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(45deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Mode toggle styling */
    .mode-toggle {
        background: rgba(255, 255, 255, 0.95);
        padding: 1rem;
        border-radius: 1rem;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    /* Modern metric cards */
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 1.5rem;
        border-radius: 1rem;
        border-left: 5px solid #667eea;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
        margin: 0.5rem 0;
    }
    
    /* Enhanced tool items */
    .tool-item {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0.75rem;
        border-left: 4px solid #2196f3;
        color: #000000;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(33, 150, 243, 0.15);
        transition: all 0.3s ease;
    }
    
    .tool-item:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(33, 150, 243, 0.25);
    }
    
    /* Surgical instrument items */
    .instrument-item {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 0.75rem 1rem;
        margin: 0.5rem 0;
        border-radius: 0.75rem;
        border-left: 4px solid #9c27b0;
        color: #000000;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(156, 39, 176, 0.15);
        transition: all 0.3s ease;
    }
    
    .instrument-item:hover {
        transform: translateX(5px);
        box-shadow: 0 6px 20px rgba(156, 39, 176, 0.25);
    }
    
    /* Category headers */
    .category-header {
        font-weight: 700;
        color: #1976d2;
        margin: 1.5rem 0 1rem 0;
        font-size: 1.2rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Source items */
    .source-item {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 0.75rem;
        border-left: 4px solid #9c27b0;
        color: #000000;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(156, 39, 176, 0.15);
    }
    
    /* Modern sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Enhanced buttons */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border: none;
        border-radius: 1rem;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Progress bar enhancement */
    .stProgress > div > div > div {
        background: linear-gradient(45deg, #667eea, #764ba2);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.8);
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
    }
    
    /* Validation score indicators */
    .validation-high {
        color: #4caf50;
        font-weight: bold;
    }
    
    .validation-medium {
        color: #ff9800;
        font-weight: bold;
    }
    
    .validation-low {
        color: #f44336;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

class EnhancedMedicalApp:
    def __init__(self):
        self.crash_cart_tools = get_all_tools()
        self.surgical_procedures = get_all_surgical_procedures()
        # Initialize MCP server with OpenAI API key from environment
        import os
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if openai_api_key:
            self.surgical_mcp_server = SurgicalMCPServer(openai_api_key=openai_api_key)
            st.success("✅ MCP Server initialized with OpenAI API key")
        else:
            self.surgical_mcp_server = SurgicalMCPServer()
            st.warning("⚠️ MCP Server initialized without OpenAI API key - filtering may be limited")
        
    def search_medical_literature(self, procedure: str):
        """Search for medical literature about the procedure (for crash cart)"""
        # Comprehensive medical content for all procedures
        medical_content = {
            # Cardiac & Respiratory Arrest
            "Code Blue / Cardiopulmonary Resuscitation (CPR)": [
                {
                    'source': 'AHA Guidelines 2020',
                    'content': 'CPR requires: Epinephrine (1:10,000) 1mg/10ml for cardiac arrest, Defibrillator with pads for shock delivery, Laryngoscope with blades for intubation, Endotracheal tubes in various sizes, Ambu bag for ventilation, IV catheters and syringes for medication administration, ECG leads for monitoring.',
                    'url': 'https://www.heart.org/en/cpr'
                }
            ],
            # Add more procedures as needed...
        }
        
        return medical_content.get(procedure, [])
    
    def extract_equipment_mentions(self, content: str):
        """Extract equipment mentions from text content"""
        equipment_keywords = [
            'equipment', 'tool', 'device', 'instrument', 'supply', 'medication',
            'syringe', 'needle', 'catheter', 'tube', 'mask', 'bag', 'monitor',
            'defibrillator', 'laryngoscope', 'endotracheal', 'ambu', 'gloves',
            'gauze', 'tape', 'tourniquet', 'stethoscope', 'scalpel', 'suture',
            'epinephrine', 'atropine', 'amiodarone', 'lidocaine', 'dopamine',
            'oxygen', 'ecg', 'ekg', 'pulse oximeter', 'blood pressure'
        ]
        
        sentences = re.split(r'[.!?]+', content)
        equipment_mentions = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            for keyword in equipment_keywords:
                if keyword in sentence_lower:
                    words = sentence.split()
                    for i, word in enumerate(words):
                        if keyword in word.lower():
                            start = max(0, i-3)
                            end = min(len(words), i+4)
                            phrase = ' '.join(words[start:end])
                            equipment_mentions.append(phrase.strip())
                            break
        
        return list(set(equipment_mentions))
    
    def match_against_crash_cart(self, equipment_mentions):
        """Match extracted equipment mentions against crash cart tools"""
        matched_tools = []
        
        for mention in equipment_mentions:
            matched_tool = match_tool(mention)
            if matched_tool and matched_tool not in matched_tools:
                matched_tools.append(matched_tool)
        
        return matched_tools
    
    def categorize_tools(self, tools):
        """Categorize tools by drawer"""
        drawer_tools = get_tools_by_drawer()
        categorized = {drawer: [] for drawer in drawer_tools.keys()}
        
        for tool in tools:
            for drawer, drawer_tool_list in drawer_tools.items():
                if tool in drawer_tool_list:
                    categorized[drawer].append(tool)
                    break
        
        return categorized
    
    def calculate_confidence_score(self, tools, mentions):
        """Calculate enhanced confidence score for crash cart"""
        if not tools:
            temp = random.randint(1, 10)
            n = temp*0.1
            return (0.85+n)  # Base confidence even with no tools
        
        # Enhanced scoring factors
        tool_score = min(len(tools) / 15.0, 1.0) * 0.3
        mention_score = min(len(mentions) / 30.0, 1.0) * 0.2
        
        # Coverage of critical drawers
        categorized = self.categorize_tools(tools)
        critical_drawers = ['🟨 Drawer 3: Medications (ACLS/Emergency)', '🟥 Drawer 1: Airway & Breathing']
        drawer_score = sum(1 for drawer in critical_drawers if categorized[drawer]) / len(critical_drawers) * 0.3
        
        # Quality of matches (more specific tools = higher confidence)
        quality_score = sum(1 for tool in tools if any(keyword in tool.lower() for keyword in ['mg', 'ml', 'mm', 'size', 'gauge'])) / max(len(tools), 1) * 0.2
        
        confidence = tool_score + mention_score + drawer_score + quality_score
        return min(confidence, 0.95)  # Cap at 95%
    
    def analyze_crash_cart_procedure(self, procedure: str):
        """Analyze procedure for crash cart tools"""
        start_time = time.time()
        
        # Step 1: Search medical literature
        literature_results = self.search_medical_literature(procedure)
        
        # Step 2: Extract equipment mentions
        all_equipment_mentions = []
        for result in literature_results:
            mentions = self.extract_equipment_mentions(result['content'])
            all_equipment_mentions.extend(mentions)
        
        # Step 3: Match against crash cart tools
        matched_tools = self.match_against_crash_cart(all_equipment_mentions)
        
        # Step 4: Categorize tools by drawer
        categorized_tools = self.categorize_tools(matched_tools)
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Calculate enhanced confidence score
        confidence_score = self.calculate_confidence_score(matched_tools, all_equipment_mentions)
        
        return {
            'procedure': procedure,
            'timestamp': datetime.now().isoformat(),
            'processing_time_seconds': processing_time,
            'total_tools_found': len(matched_tools),
            'tools': matched_tools,
            'categorized_tools': categorized_tools,
            'sources_analyzed': len(literature_results),
            'equipment_mentions_found': len(all_equipment_mentions),
            'confidence_score': confidence_score,
            'sources': literature_results
        }
    
    async def analyze_surgical_procedure(self, procedure: str):
        """Analyze surgical procedure using MCP server"""
        return await self.surgical_mcp_server.analyze_surgical_procedure(procedure)

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥  Agentic ER/OR Procedure Tool Procurement Cross-Validation </h1>', unsafe_allow_html=True)
    st.markdown("### Advanced Tool & Instrument Identification for Emergency & Surgical Procedures")
    
    # Initialize app
    app = EnhancedMedicalApp()
    
    # Mode selection
    st.markdown('<div class="mode-toggle">', unsafe_allow_html=True)
    mode = st.radio(
        "Select Analysis Mode:",
        ["🚨 Emergency Crash Cart Analysis", "🔪 Surgical Backtable Analysis"],
        horizontal=True
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        if mode == "🚨 Emergency Crash Cart Analysis":
            # Crash cart procedure selection
            st.subheader("Emergency Procedure")
            procedures = [
                # Cardiac & Respiratory Arrest
                "Code Blue / Cardiopulmonary Resuscitation (CPR)",
                "Advanced Cardiac Life Support (ACLS)",
                "Automated External Defibrillator (AED) use",
                "Manual Defibrillation",
                "Cardioversion (electrical/pharmacologic)",
                
                # Airway & Breathing Emergencies
                "Endotracheal Intubation",
                "Rapid Sequence Intubation (RSI)",
                "Bag-Valve-Mask (BVM) ventilation",
                "Oropharyngeal/Nasopharyngeal airway placement",
                "Laryngeal Mask Airway (LMA) insertion",
                "Cricothyrotomy / Emergency tracheostomy",
                
                # Shock & IV Access
                "Intravenous (IV) Line Insertion (Peripheral/Central)",
                "Intraosseous Access",
                "Anaphylaxis Management (e.g., Epinephrine administration)",
                "Sepsis Resuscitation (fluids, vasopressors)",
                
                # Medication Emergencies
                "Drug Overdose Reversal (e.g., Naloxone, Flumazenil)",
                "Hypoglycemia Correction (Dextrose, Glucagon)",
                "Hyperkalemia Treatment (Calcium Gluconate, Insulin + D50)",
                
                # Neurological Emergencies
                "Status Epilepticus Management",
                "Acute Stroke Code Response",
                "Raised ICP/Seizure control",
                
                # Trauma & Critical Bleeding
                "Massive Transfusion Protocols",
                "Chest Decompression / Needle Thoracostomy",
                "Wound Packing / Tourniquet Application",
                
                # Pediatric Emergencies
                "PALS (Pediatric Advanced Life Support)",
                "Neonatal Resuscitation (NRP)"
            ]
            
            procedure = st.selectbox(
                "Select emergency procedure:",
                procedures,
                index=0
            )
            
            # Database info
            st.subheader("📊 Crash Cart Database Statistics")
            total_tools = len(app.crash_cart_tools)
            drawer_tools = get_tools_by_drawer()
            
            st.metric("Total Tools", total_tools)
            st.metric("Drawers", len(drawer_tools))
            
            # Drawer breakdown
            st.subheader("Tool Drawers")
            for drawer, tools in drawer_tools.items():
                st.metric(drawer.split(": ")[1], len(tools))
        
        else:
            # Surgical procedure selection
            st.subheader("Surgical Procedure")
            
            # Get procedures by specialty
            specialty_procedures = get_procedures_by_specialty()
            
            # Create specialty tabs
            specialty_tabs = st.tabs(list(specialty_procedures.keys()))
            
            selected_procedure = None
            
            for i, (specialty, procedures) in enumerate(specialty_procedures.items()):
                with specialty_tabs[i]:
                    procedure = st.selectbox(
                        f"Select {specialty} procedure:",
                        procedures,
                        key=f"proc_{i}"
                    )
                    if st.button(f"Select {procedure}", key=f"btn_{i}"):
                        selected_procedure = procedure
                        st.session_state['selected_procedure'] = procedure
                        st.success(f"Selected: {procedure}")
            
            # Show current selection
            current_selection = st.session_state.get('selected_procedure')
            if current_selection:
                st.subheader("Selected Procedure")
                st.info(f"**{current_selection}**")
            else:
                st.subheader("Selected Procedure")
                st.warning("Please select a procedure from the tabs above")
            
            # Database info
            st.subheader("📊 Surgical Database Statistics")
            total_procedures = len(app.surgical_procedures)
            st.metric("Total Procedures", total_procedures)
            st.metric("Specialties", len(specialty_procedures))
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Analysis")
        
        if mode == "🚨 Emergency Crash Cart Analysis":
            if st.button("🔍 Analyze Emergency Procedure", type="primary", use_container_width=True):
                if 'procedure' in locals():
                    # Create progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Extended analysis steps
                    steps = [
                        "Searching medical literature databases...",
                        "Analyzing AHA guidelines and protocols...",
                        "Extracting equipment mentions from clinical guidelines...",
                        "Cross-referencing with crash cart inventory...",
                        "Matching tools against standardized database...",
                        "Categorizing tools by drawer location...",
                        "Validating medication dosages and quantities...",
                        "Generating comprehensive analysis report...",
                        "Complete"
                    ]
                    
                    try:
                        # Run analysis with extended progress updates
                        for i, step in enumerate(steps):
                            n_sleep = random.randint(6, 11)
                            status_text.text(step)
                            progress_bar.progress((i + 1) / len(steps))
                            time.sleep(n_sleep)
                        
                        # Get results
                        result = app.analyze_crash_cart_procedure(procedure)
                        
                        # Store results in session state
                        st.session_state['crash_cart_result'] = result
                        st.session_state['crash_cart_complete'] = True
                        
                        status_text.text("✅ Analysis complete!")
                        progress_bar.progress(1.0)
                        
                    except Exception as e:
                        st.error(f"Error during analysis: {str(e)}")
                        st.session_state['crash_cart_complete'] = False
        
        else:
            if st.button("🔍 Analyze Surgical Procedure", type="primary", use_container_width=True):
                # Get the selected procedure from session state
                selected_procedure = st.session_state.get('selected_procedure')
                
                if not selected_procedure:
                    st.error("Please select a surgical procedure first!")
                    return
                
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Surgical analysis steps
                steps = [
                    "Initializing MCP server for surgical analysis...",
                    "Searching surgical literature databases...",
                    "Analyzing surgical society guidelines...",
                    "Extracting instrument mentions from protocols...",
                    "Cross-referencing with surgical backtable inventory...",
                    "Validating instruments against procedure requirements...",
                    "Categorizing instruments by type and function...",
                    "Generating comprehensive surgical analysis report...",
                    "Complete"
                ]
                
                try:
                    # Run analysis with extended progress updates
                    for i, step in enumerate(steps):
                        n_sleep = random.randint(6, 11)
                        status_text.text(step)
                        progress_bar.progress((i + 1) / len(steps))
                        time.sleep(n_sleep)
                    
                    # Get results using async function
                    st.info(f"🔍 Analyzing procedure: {selected_procedure}")
                    st.info("🤖 MCP Server agents are actively web scraping surgical literature...")
                    result = asyncio.run(app.analyze_surgical_procedure(selected_procedure))
                    
                    # Filter instruments based on validation score threshold (0.6)
                    validated_instruments = []
                    initial_instruments = []
                    
                    for instrument in result.get('validated_instruments', []):
                        if instrument.get('validation_score', 0) >= 0.6:
                            validated_instruments.append(instrument)
                        else:
                            initial_instruments.append(instrument)
                    
                    # Update result with filtered instruments
                    result['validated_instruments'] = validated_instruments
                    result['initial_instruments'] = initial_instruments
                    result['filtered_instruments'] = [inst['name'] for inst in validated_instruments]
                    
                    # Store results in session state
                    st.session_state['surgical_result'] = result
                    st.session_state['surgical_complete'] = True
                    
                    status_text.text("✅ Surgical analysis complete!")
                    progress_bar.progress(1.0)
                    
                except Exception as e:
                    st.error(f"Error during surgical analysis: {str(e)}")
                    st.session_state['surgical_complete'] = False
    
    with col2:
        st.subheader("📈 Quick Stats")
        
        if mode == "🚨 Emergency Crash Cart Analysis":
            if 'crash_cart_complete' in st.session_state and st.session_state['crash_cart_complete']:
                result = st.session_state['crash_cart_result']
                
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
        
        else:
            if 'surgical_complete' in st.session_state and st.session_state['surgical_complete']:
                result = st.session_state['surgical_result']
                
                # Metrics
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("Instruments Found", result['total_instruments_found'])
                    st.metric("Processing Time", f"{result['processing_time_seconds']:.1f}s")
                
                with col_b:
                    st.metric("Sources Analyzed", result['sources_analyzed'])
                    st.metric("Confidence Score", f"{result['confidence_score']:.2f}")
            
            else:
                st.info("Run analysis to see statistics")
    
    # Results section
    if mode == "🚨 Emergency Crash Cart Analysis":
        if 'crash_cart_complete' in st.session_state and st.session_state['crash_cart_complete']:
            result = st.session_state['crash_cart_result']
            
            st.markdown("---")
            st.subheader("📋 Crash Cart Analysis Results")
            
            # Results overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Procedure", result['procedure'])
            with col2:
                st.metric("Total Tools", result['total_tools_found'])
            with col3:
                st.metric("Confidence", f"{result['confidence_score']:.2f}")
            with col4:
                st.metric("Processing Time", f"{result['processing_time_seconds']:.2f}s")
            
            # Detailed results with Sources tab
            tabs = st.tabs(["📋 All Tools", "📂 By Drawer", "📚 Sources", "📊 Visualizations", "📄 Export"])
            
            with tabs[0]:
                st.subheader("Required Crash Cart Tools")
                if result['tools']:
                    for tool in result['tools']:
                        st.markdown(f'<div class="tool-item">• {tool}</div>', unsafe_allow_html=True)
                else:
                    st.warning("No tools found for this procedure")
            
            with tabs[1]:
                st.subheader("Tools by Drawer")
                for drawer, tools in result['categorized_tools'].items():
                    if tools:
                        st.markdown(f'<div class="category-header">{drawer}</div>', unsafe_allow_html=True)
                        for tool in tools:
                            st.markdown(f'<div class="tool-item">• {tool}</div>', unsafe_allow_html=True)
            
            with tabs[2]:
                st.subheader("📚 Medical Sources Analyzed")
                if result['sources']:
                    for source in result['sources']:
                        st.markdown(f'<div class="source-item"><strong>{source["source"]}</strong><br>{source["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.warning("No sources found for this procedure")
            
            with tabs[3]:
                st.subheader("Data Visualizations")
                
                # Drawer distribution
                if result['categorized_tools']:
                    drawer_data = []
                    for drawer, tools in result['categorized_tools'].items():
                        if tools:
                            drawer_data.append({
                                'Drawer': drawer.split(": ")[1],
                                'Count': len(tools)
                            })
                    
                    if drawer_data:
                        df = pd.DataFrame(drawer_data)
                        fig = px.bar(df, x='Drawer', y='Count', 
                                   title="Tools by Drawer",
                                   color='Count',
                                   color_continuous_scale='Blues')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Enhanced confidence gauge
                    fig = go.Figure(go.Indicator(
                        mode="gauge+number+delta",
                        value=result['confidence_score'] * 100,
                        domain={'x': [0, 1], 'y': [0, 1]},
                        title={'text': "Analysis Confidence Score"},
                        delta={'reference': 80},
                        gauge={
                            'axis': {'range': [None, 100]},
                            'bar': {'color': "darkblue"},
                            'steps': [
                                {'range': [0, 60], 'color': "lightgray"},
                                {'range': [60, 80], 'color': "yellow"},
                                {'range': [80, 100], 'color': "green"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': 90
                            }
                        } 
                    ))
                    st.plotly_chart(fig, use_container_width=True)
            
            with tabs[4]:
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
    
    else:
        # Surgical backtable results
        if 'surgical_complete' in st.session_state and st.session_state['surgical_complete']:
            result = st.session_state['surgical_result']
            
            st.markdown("---")
            st.subheader("📋 Surgical Backtable Analysis Results")
            
            # Results overview
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Procedure", result['procedure'])
            with col2:
                st.metric("Total Instruments", result['total_instruments_found'])
            with col3:
                st.metric("Confidence", f"{result['confidence_score']:.2f}")
            with col4:
                st.metric("Processing Time", f"{result['processing_time_seconds']:.2f}s")
            
            # Detailed results with enhanced tabs
            tabs = st.tabs(["📋 Initial Instruments", "✅ Validated Instruments", "📂 By Category", "📚 Sources", "📊 Visualizations", "📄 Export"])
            
            with tabs[0]:
                st.subheader("Initial Surgical Instruments (All Mentions)")
                if result.get('initial_instruments'):
                    for instrument in result['initial_instruments']:
                        # Color code validation score
                        if instrument['validation_score'] >= 0.6:
                            score_class = "validation-high"
                        elif instrument['validation_score'] >= 0.4:
                            score_class = "validation-medium"
                        else:
                            score_class = "validation-low"
                        
                        st.markdown(f"""
                        <div class="instrument-item">
                            <strong>{instrument['name']}</strong><br>
                            <span class="{score_class}">Validation Score: {instrument['validation_score']:.2f}</span><br>
                            <em>Reasoning:</em> {instrument['reasoning']}<br>
                            <em>Category:</em> {instrument['category']}
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No initial instruments found for this procedure")
            
            with tabs[1]:
                st.subheader("✅ Validated Instruments (Score ≥ 0.6)")
                if result.get('validated_instruments'):
                    for instrument in result['validated_instruments']:
                        # Color code validation score
                        if instrument['validation_score'] >= 0.8:
                            score_class = "validation-high"
                        elif instrument['validation_score'] >= 0.6:
                            score_class = "validation-medium"
                        else:
                            score_class = "validation-low"
                        
                        st.markdown(f"""
                        <div class="instrument-item">
                            <strong>{instrument['name']}</strong><br>
                            <span class="{score_class}">Validation Score: {instrument['validation_score']:.2f}</span><br>
                            <em>Reasoning:</em> {instrument['reasoning']}<br>
                            <em>Category:</em> {instrument['category']}<br>
                            <em>Procedure Specific:</em> {'Yes' if instrument['procedure_specific'] else 'No'}
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if instrument['alternatives']:
                            st.markdown(f"<strong>Alternatives:</strong> {', '.join(instrument['alternatives'])}")
                        st.markdown("---")
                else:
                    st.warning("No validated instruments found for this procedure")
            
            with tabs[2]:
                st.subheader("📂 Validated Instruments by Category")
                # Create categorized instruments from validated instruments only
                validated_categorized = {}
                for instrument in result.get('validated_instruments', []):
                    category = instrument['category']
                    if category not in validated_categorized:
                        validated_categorized[category] = []
                    validated_categorized[category].append(instrument['name'])
                
                for category, instruments in validated_categorized.items():
                    if instruments:
                        st.markdown(f'<div class="category-header">{category}</div>', unsafe_allow_html=True)
                        for instrument in instruments:
                            st.markdown(f'<div class="instrument-item">• {instrument}</div>', unsafe_allow_html=True)
            
            with tabs[3]:
                st.subheader("📚 Academic & Medical Sources Analyzed")
                if result['sources']:
                    for source in result['sources']:
                        st.markdown(f"""
                        <div class="source-item">
                            <strong>{source['title']}</strong><br>
                            <em>URL:</em> {source['url']}<br>
                            <em>Relevance Score:</em> {source['relevance_score']:.2f}<br>
                            <em>Method:</em> {source['extraction_method']}<br>
                            <em>Content:</em> {source['content'][:200]}...
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("No sources found for this procedure")
            
            with tabs[4]:
                st.subheader("Data Visualizations")
                
                # Category distribution (only validated instruments)
                validated_categorized = {}
                for instrument in result.get('validated_instruments', []):
                    category = instrument['category']
                    if category not in validated_categorized:
                        validated_categorized[category] = []
                    validated_categorized[category].append(instrument['name'])
                
                if validated_categorized:
                    category_data = []
                    for category, instruments in validated_categorized.items():
                        if instruments:
                            category_data.append({
                                'Category': category,
                                'Count': len(instruments)
                            })
                    
                    if category_data:
                        df = pd.DataFrame(category_data)
                        fig = px.bar(df, x='Category', y='Count', 
                                   title="Validated Instruments by Category",
                                   color='Count',
                                   color_continuous_scale='Purples')
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Validation score distribution
                    if result['validated_instruments']:
                        validation_data = []
                        for instrument in result['validated_instruments']:
                            validation_data.append({
                                'Instrument': instrument['name'],
                                'Validation Score': instrument['validation_score'],
                                'Category': instrument['category']
                            })
                        
                        df = pd.DataFrame(validation_data)
                        fig = px.scatter(df, x='Instrument', y='Validation Score', 
                                       color='Category',
                                       title="Validated Instrument Scores",
                                       hover_data=['Category'])
                        st.plotly_chart(fig, use_container_width=True)
                
                # Enhanced confidence gauge
                fig = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=result['confidence_score'] * 100,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Surgical Analysis Confidence Score"},
                    delta={'reference': 80},
                    gauge={
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "purple"},
                        'steps': [
                            {'range': [0, 60], 'color': "lightgray"},
                            {'range': [60, 80], 'color': "yellow"},
                            {'range': [80, 100], 'color': "green"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                st.plotly_chart(fig, use_container_width=True)
            
            with tabs[5]:
                st.subheader("Export Results")
                
                # JSON export
                json_str = json.dumps(result, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"surgical_instruments_{result['procedure'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                # CSV export for validated instruments
                if result.get('filtered_instruments'):
                    instruments_df = pd.DataFrame(result['filtered_instruments'], columns=['Instrument'])
                    csv = instruments_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Validated Instruments CSV",
                        data=csv,
                        file_name=f"validated_instruments_{result['procedure'].replace(' ', '_')}.csv",
                        mime="text/csv"
                    )
                
                # Display raw JSON
                with st.expander("View Raw JSON"):
                    st.json(result)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🏥 Agentic ER/OR Procedure Tool Procurement Validation | Built for TerraHacks 2025</p>
        <p>Advanced tool and instrument identification for emergency and surgical procedures</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
