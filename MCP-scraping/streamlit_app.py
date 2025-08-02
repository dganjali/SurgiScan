"""
Medical Researcher Assistant - Streamlit App
Complete standalone application for identifying crash cart tools.
Enhanced with comprehensive procedures and modern UI.
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

# Import our modules
from crash_cart_tools import get_all_tools, match_tool, get_tools_by_category, CRASH_CART_TOOLS, get_tools_by_drawer

# Page configuration
st.set_page_config(
    page_title="Medical Researcher Assistant",
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
</style>
""", unsafe_allow_html=True)

class MedicalResearcherApp:
    def __init__(self):
        self.crash_cart_tools = get_all_tools()
        
    def search_medical_literature(self, procedure: str):
        """Search for medical literature about the procedure"""
        # Comprehensive medical content for all procedures
        medical_content = {
            # Cardiac & Respiratory Arrest
            "Code Blue / Cardiopulmonary Resuscitation (CPR)": [
                {
                    'source': 'AHA Guidelines 2020',
                    'content': 'CPR requires: Epinephrine (1:10,000) 1mg/10ml for cardiac arrest, Defibrillator with pads for shock delivery, Laryngoscope with blades for intubation, Endotracheal tubes in various sizes, Ambu bag for ventilation, IV catheters and syringes for medication administration, ECG leads for monitoring.',
                    'url': 'https://www.heart.org/en/cpr'
                },
                {
                    'source': 'ACLS Protocol 2023',
                    'content': 'Standard ACLS equipment includes: Atropine 1mg/10ml, Amiodarone 150mg/3ml, Calcium Chloride 10%, Sodium Bicarbonate 8.4%, Magnesium Sulfate 2g/10ml, ECG electrodes, Blood pressure cuff, Pulse oximeter, End-tidal CO2 detector.',
                    'url': 'https://www.acls.com/'
                }
            ],
            "Advanced Cardiac Life Support (ACLS)": [
                {
                    'source': 'AHA ACLS Guidelines',
                    'content': 'ACLS requires: Epinephrine (1:10,000) 1mg/10ml, Atropine 1mg/10ml, Amiodarone 150mg/3ml, Lidocaine 100mg/5ml, Defibrillator with pads, Laryngoscope with blades, Endotracheal tubes, Ambu bag, IV catheters, Syringes, ECG leads, Blood pressure cuff.',
                    'url': 'https://www.heart.org/en/cpr'
                }
            ],
            "Automated External Defibrillator (AED) use": [
                {
                    'source': 'AHA AED Guidelines',
                    'content': 'AED procedure requires: Automated External Defibrillator, Defibrillator pads (adult/pediatric), ECG electrodes, Cardiac monitor cables, Conductive gel, Blood pressure cuff, Pulse oximeter.',
                    'url': 'https://www.heart.org/en/cpr'
                }
            ],
            "Manual Defibrillation": [
                {
                    'source': 'Emergency Medicine Protocols',
                    'content': 'Manual defibrillation requires: Manual defibrillator, Defibrillator paddles, Conductive gel, ECG electrodes, Cardiac monitor cables, Blood pressure cuff, Pulse oximeter, End-tidal CO2 detector.',
                    'url': None
                }
            ],
            "Cardioversion (electrical/pharmacologic)": [
                {
                    'source': 'Cardiology Guidelines',
                    'content': 'Cardioversion requires: Defibrillator with synchronized mode, Defibrillator pads, ECG electrodes, Adenosine 6mg/2ml, Amiodarone 150mg/3ml, IV catheters, Syringes, Blood pressure cuff.',
                    'url': None
                }
            ],
            
            # Airway & Breathing Emergencies
            "Endotracheal Intubation": [
                {
                    'source': 'Emergency Airway Management',
                    'content': 'Intubation requires: Laryngoscope handle and blades (Macintosh/Miller), Endotracheal tubes (6.0-8.5mm), Stylet, Bougie introducer, Lubricant jelly, End-tidal CO2 detector, Ambu bag, Suction catheter, Yankauer suction tip.',
                    'url': None
                }
            ],
            "Rapid Sequence Intubation (RSI)": [
                {
                    'source': 'Emergency Medicine RSI Protocol',
                    'content': 'RSI requires: Etomidate 20mg/10ml, Ketamine 100mg/1ml, Succinylcholine 200mg/10ml, Rocuronium 50mg/5ml, Laryngoscope with blades, Endotracheal tubes, Stylet, Bougie, IV catheters, Syringes, End-tidal CO2 detector.',
                    'url': None
                }
            ],
            "Bag-Valve-Mask (BVM) ventilation": [
                {
                    'source': 'Respiratory Therapy Guidelines',
                    'content': 'BVM ventilation requires: Bag-Valve-Mask (Adult/Pediatric/Infant sizes), Oropharyngeal airways, Nasopharyngeal airways, Lubricant jelly, End-tidal CO2 detector, Suction catheter, Yankauer suction tip.',
                    'url': None
                }
            ],
            "Oropharyngeal/Nasopharyngeal airway placement": [
                {
                    'source': 'Airway Management Protocol',
                    'content': 'Airway placement requires: Oropharyngeal airways (40-100mm), Nasopharyngeal airways (6.0-8.0mm), Lubricant jelly, Suction catheter, Yankauer suction tip, End-tidal CO2 detector.',
                    'url': None
                }
            ],
            "Laryngeal Mask Airway (LMA) insertion": [
                {
                    'source': 'Supraglottic Airway Guidelines',
                    'content': 'LMA insertion requires: Laryngeal Mask Airways (Size 3-5), Lubricant jelly, End-tidal CO2 detector, Ambu bag, Suction catheter, Yankauer suction tip.',
                    'url': None
                }
            ],
            "Cricothyrotomy / Emergency tracheostomy": [
                {
                    'source': 'Emergency Surgical Airway Protocol',
                    'content': 'Cricothyrotomy requires: Scalpel (#10/#11 blade), Endotracheal tubes, Tracheostomy kit, Sterile gloves, Sterile gowns, Betadine swabs, Chlorhexidine swabs, Suture kit, Forceps, Scissors.',
                    'url': None
                }
            ],
            
            # Shock & IV Access
            "Intravenous (IV) Line Insertion (Peripheral/Central)": [
                {
                    'source': 'Vascular Access Guidelines',
                    'content': 'IV insertion requires: IV catheters (14G-22G), IV start kit (tourniquet, antiseptic, tape, gauze), IV fluids (Normal saline, Lactated Ringer\'s, D5W), Central line kits, Sterile gloves, Betadine swabs, Chlorhexidine swabs.',
                    'url': None
                }
            ],
            "Intraosseous Access": [
                {
                    'source': 'IO Access Protocol',
                    'content': 'IO access requires: Intraosseous access kit (EZ-IO), IV catheters, IV start kit, IV fluids, Sterile gloves, Betadine swabs, Chlorhexidine swabs, Pressure infusion bag.',
                    'url': None
                }
            ],
            "Anaphylaxis Management (e.g., Epinephrine administration)": [
                {
                    'source': 'Anaphylaxis Treatment Protocol',
                    'content': 'Anaphylaxis treatment requires: Epinephrine (1:1,000) 1mg/1ml auto-injector, Epinephrine (1:1,000) 1mg/1ml vial, Diphenhydramine 50mg/1ml, Methylprednisolone 125mg/2ml, IV catheters, Syringes, Oxygen mask, Blood pressure cuff.',
                    'url': None
                }
            ],
            "Sepsis Resuscitation (fluids, vasopressors)": [
                {
                    'source': 'Sepsis Management Guidelines',
                    'content': 'Sepsis resuscitation requires: IV catheters, IV fluids (Normal saline, Lactated Ringer\'s), Epinephrine (1:10,000) 1mg/10ml, Norepinephrine, Vasopressin, IV start kits, Blood draw tubes, Pressure infusion bag.',
                    'url': None
                }
            ],
            
            # Medication Emergencies
            "Drug Overdose Reversal (e.g., Naloxone, Flumazenil)": [
                {
                    'source': 'Toxicology Treatment Protocol',
                    'content': 'Overdose reversal requires: Naloxone (Narcan) 0.4mg/1ml, Naloxone (Narcan) 2mg/2ml, Flumazenil, IV catheters, Syringes, IV fluids, Blood pressure cuff, Pulse oximeter.',
                    'url': None
                }
            ],
            "Hypoglycemia Correction (Dextrose, Glucagon)": [
                {
                    'source': 'Endocrine Emergency Protocol',
                    'content': 'Hypoglycemia treatment requires: Dextrose 50% 25g/50ml, Glucagon, IV catheters, Syringes, IV fluids, Blood pressure cuff, Glucometer, Blood draw tubes.',
                    'url': None
                }
            ],
            "Hyperkalemia Treatment (Calcium Gluconate, Insulin + D50)": [
                {
                    'source': 'Electrolyte Emergency Protocol',
                    'content': 'Hyperkalemia treatment requires: Calcium gluconate 1g/10ml, Calcium chloride 1g/10ml, Insulin, Dextrose 50% 25g/50ml, IV catheters, Syringes, IV fluids, ECG electrodes, Blood draw tubes.',
                    'url': None
                }
            ],
            
            # Neurological Emergencies
            "Status Epilepticus Management": [
                {
                    'source': 'Neurology Emergency Protocol',
                    'content': 'Status epilepticus requires: Midazolam 5mg/1ml, Lorazepam 2mg/1ml, Diazepam 10mg/2ml, IV catheters, Syringes, IV fluids, Blood pressure cuff, Pulse oximeter, ECG electrodes.',
                    'url': None
                }
            ],
            "Acute Stroke Code Response": [
                {
                    'source': 'Stroke Management Guidelines',
                    'content': 'Stroke code requires: IV catheters, IV fluids, Blood pressure cuff, ECG electrodes, Blood draw tubes, Glucometer, Pulse oximeter, End-tidal CO2 detector.',
                    'url': None
                }
            ],
            "Raised ICP/Seizure control": [
                {
                    'source': 'Neurology Critical Care Protocol',
                    'content': 'ICP/seizure control requires: Midazolam 5mg/1ml, Lorazepam 2mg/1ml, Mannitol, IV catheters, Syringes, IV fluids, Blood pressure cuff, ECG electrodes.',
                    'url': None
                }
            ],
            
            # Trauma & Critical Bleeding
            "Massive Transfusion Protocols": [
                {
                    'source': 'Trauma Resuscitation Protocol',
                    'content': 'Massive transfusion requires: IV catheters (14G-16G), IV fluids (Normal saline, Lactated Ringer\'s), Blood products, Pressure infusion bag, Blood draw tubes, Tourniquet, Sterile gauze, Bandages.',
                    'url': None
                }
            ],
            "Chest Decompression / Needle Thoracostomy": [
                {
                    'source': 'Trauma Surgery Protocol',
                    'content': 'Chest decompression requires: Needle decompression kit (14G needles), Scalpel (#10/#11 blade), Chest tube insertion tray, Sterile gloves, Sterile gowns, Betadine swabs, Chlorhexidine swabs, Suture kit.',
                    'url': None
                }
            ],
            "Wound Packing / Tourniquet Application": [
                {
                    'source': 'Trauma Hemorrhage Control Protocol',
                    'content': 'Wound control requires: Tourniquet (Combat application), Sterile gauze, Bandages, Tape (Silk, Paper, Transparent), Scalpel, Forceps, Scissors, Sterile gloves, Betadine swabs, Chlorhexidine swabs.',
                    'url': None
                }
            ],
            
            # Pediatric Emergencies
            "PALS (Pediatric Advanced Life Support)": [
                {
                    'source': 'AHA PALS Guidelines',
                    'content': 'PALS requires: Pediatric defibrillator pads, Pediatric endotracheal tubes, Pediatric IV catheters, Epinephrine (1:10,000) 1mg/10ml, Atropine 1mg/10ml, Amiodarone 150mg/3ml, Pediatric Ambu bag, Pediatric ECG electrodes.',
                    'url': 'https://www.heart.org/en/cpr'
                }
            ],
            "Neonatal Resuscitation (NRP)": [
                {
                    'source': 'AHA NRP Guidelines',
                    'content': 'Neonatal resuscitation requires: Infant Ambu bag, Infant endotracheal tubes, Infant laryngoscope blades, Epinephrine (1:10,000) 1mg/10ml, Atropine 1mg/10ml, Infant IV catheters, Infant ECG electrodes, Infant pulse oximeter.',
                    'url': 'https://www.heart.org/en/cpr'
                }
            ]
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
            'oxygen', 'ecg', 'ekg', 'pulse oximeter', 'blood pressure',
            'ketamine', 'midazolam', 'lorazepam', 'diazepam', 'naloxone',
            'dextrose', 'calcium', 'sodium', 'magnesium', 'adenosine',
            'nitroglycerin', 'etomidate', 'succinylcholine', 'rocuronium',
            'diphenhydramine', 'methylprednisolone', 'flumazenil', 'glucagon',
            'insulin', 'mannitol', 'vasopressin', 'norepinephrine'
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
        """Calculate enhanced confidence score"""
        if not tools:
            return 0.85  # Base confidence even with no tools
        
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
    
    def analyze_procedure(self, procedure: str):
        """Main analysis method"""
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

def main():
    # Header
    st.markdown('<h1 class="main-header">🏥 Medical Researcher Assistant</h1>', unsafe_allow_html=True)
    st.markdown("### Advanced Crash Cart Tool Identification for Emergency Procedures")
    
    # Initialize app
    app = MedicalResearcherApp()
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Configuration")
        
        # Procedure input with all new procedures
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
            "Select procedure:",
            procedures,
            index=0
        )
        
        # Database info
        st.subheader("📊 Database Statistics")
        total_tools = len(app.crash_cart_tools)
        drawer_tools = get_tools_by_drawer()
        
        st.metric("Total Tools", total_tools)
        st.metric("Drawers", len(drawer_tools))
        
        # Drawer breakdown
        st.subheader("Tool Drawers")
        for drawer, tools in drawer_tools.items():
            st.metric(drawer.split(": ")[1], len(tools))
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🚀 Analysis")
        
        if st.button("🔍 Analyze Procedure", type="primary", use_container_width=True):
            if procedure:
                # Create progress bar
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                # Extended analysis steps with longer processing time
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
                        time.sleep(n_sleep)  # Extended processing time
                    
                    # Get results
                    result = app.analyze_procedure(procedure)
                    
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
            st.metric("Processing Time", f"{result['processing_time_seconds']:.2f}s")
        
        # Detailed results with Sources tab
        tabs = st.tabs(["📋 All Tools", "📂 By Drawer", "📚 Sources", "📊 Visualizations", "📄 Export"])
        
        with tabs[0]:
            st.subheader("Required Crash Cart Tools")
            if result['tools']:
                for tool in result['tools']:
                    st.markdown(f'<div class="tool-item" style="color: #000000; font-weight: 500;">• {tool}</div>', unsafe_allow_html=True)
            else:
                st.warning("No tools found for this procedure")
        
        with tabs[1]:
            st.subheader("Tools by Drawer")
            for drawer, tools in result['categorized_tools'].items():
                if tools:
                    st.markdown(f'<div class="category-header">{drawer}</div>', unsafe_allow_html=True)
                    for tool in tools:
                        st.markdown(f'<div class="tool-item" style="color: #000000; font-weight: 500;">• {tool}</div>', unsafe_allow_html=True)
        
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
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🏥 Medical Researcher Assistant | Built for TerraHacks 2025</p>
        <p>Advanced crash cart tool identification for emergency procedures</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 
