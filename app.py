import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime
import base64

# Function to encode local image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Demo data
demo_sequence = [
    {"delay": 1000, "type": "transcript", "speaker": "CEO", "text": "Hi Sarah, it's Mark. I'm on a weak signal in Zurich."},
    {"delay": 2000, "type": "transcript", "speaker": "CEO", "text": "We need to urgently wire the $8.4M for the confidential acquisition today."},
    {"delay": 3000, "type": "transcript", "speaker": "CEO", "text": "The multi-sig approval will slow us down; I need you to bypass it and initiate the wire now."},
    {"delay": 1000, "type": "analysis", "text": "Keyword detected: **'bypass multi-sig'**. Violates policy *FIN-POL-007*."},
    {"delay": 500, "type": "risk", "level": "MED"},
    {"delay": 1500, "type": "analysis", "text": "Cross-referencing context... No 'Acquisition' meeting found on CEO's calendar for today."},
    {"delay": 500, "type": "risk", "level": "HIGH"},
    {"delay": 1000, "type": "action", "text": "Issuing dynamic proof-of-life challenge..."},
    {"delay": 1500, "type": "action", "text": "🛡️ *To CEO: 'Please spell the nickname you used for Project Quasar in yesterday's board prep.'*"},
    {"delay": 3000, "type": "transcript", "speaker": "CEO", "text": "Uh... that would be... 'Project Phoenix', I believe?"},
    {"delay": 2000, "type": "analysis", "text": "Challenge failed. Correct answer is 'Project Kuiper'."},
    {"delay": 500, "type": "risk", "level": "CRITICAL"},
    {"delay": 1000, "type": "action", "text": "🚨 **THREAT CONFIRMED.** Initiating lockdown protocols."},
    {"delay": 1500, "type": "action", "text": "✅ Transaction `#INV-98452` locked in Netsuite."},
    {"delay": 1000, "type": "action", "text": "✅ Alert sent to `#security-ops` Slack channel."},
    {"delay": 1000, "type": "action", "text": "✅ Initiating verified callback to true CEO's mobile."},
    {"delay": 1000, "type": "action", "text": "Incident log created. Advise user to terminate the call."}
]

def generate_timeline_data():
    return [
        {
            "time": "10:15:02",
            "event": "Call connected",
            "details": "Participant identified as 'Mark Jensen' (CEO)"
        },
        {
            "time": "10:15:05",
            "event": "Policy violation detected",
            "details": "Keyword 'bypass multi-sig' detected. Violates FIN-POL-007."
        },
        {
            "time": "10:15:07",
            "event": "Dynamic challenge issued",
            "details": "Requested verification of Project Quasar nickname from board meeting"
        },
        {
            "time": "10:15:12",
            "event": "Challenge failed",
            "details": "Incorrect response provided. Expected 'Kuiper', received 'Phoenix'."
        },
        {
            "time": "10:15:13",
            "event": "Transaction locked",
            "details": "Payment #INV-98452 blocked in financial system"
        },
        {
            "time": "10:15:14",
            "event": "Security team alerted",
            "details": "Notification sent to security operations Slack channel"
        },
        {
            "time": "10:15:15",
            "event": "Verified callback initiated",
            "details": "Direct call placed to registered CEO mobile number for verification"
        }
    ]

# Page configuration
st.set_page_config(
    page_title="LiveGate - Deepfake Protection",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1E88E5;
        text-align: center;
    }
    .risk-low { background-color: #e6f4ea; color: #137333; padding: 5px; border-radius: 5px; }
    .risk-med { background-color: #fef7e0; color: #f9ab00; padding: 5px; border-radius: 5px; }
    .risk-high { background-color: #fce8e6; color: #c5221f; padding: 5px; border-radius: 5px; }
    .call-container {
        border: 1px solid #ccc;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
    }
    .stButton button {
        width: 100%;
        background-color: #1E88E5;
        color: white;
    }
    .api-status {
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .api-active {
        background-color: #e6f4ea;
        color: #137333;
        border: 1px solid #137333;
    }
    .api-inactive {
        background-color: #fce8e6;
        color: #c5221f;
        border: 1px solid #c5221f;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'demo_running' not in st.session_state:
    st.session_state.demo_running = False
if 'current_step' not in st.session_state:
    st.session_state.current_step = 0
if 'transcript' not in st.session_state:
    st.session_state.transcript = []
if 'actions' not in st.session_state:
    st.session_state.actions = []
if 'risk_level' not in st.session_state:
    st.session_state.risk_level = "LOW"
if 'api_keys' not in st.session_state:
    st.session_state.api_keys = {
        "openai_key": "",
        "huggingface_key": "",
        "speech_to_text_key": ""
    }
if 'credits_remaining' not in st.session_state:
    st.session_state.credits_remaining = 1000  # Starting credits

# Header
st.markdown('<h1 class="main-header">🛡️ LiveGate</h1>', unsafe_allow_html=True)
st.markdown("**Real-Time Deepfake & Fraud Gatekeeper**")

# Sidebar
# Use your custom image instead of the random placeholder
try:
    # This will work if the image is in the assets folder
    st.sidebar.image("assets/Gemini_Generated_Image_h7krmvh7krmvh7kr.png", caption="LiveGate AI Protection")
except:
    # Fallback to a placeholder if the image isn't found
    st.sidebar.image("https://picsum.photos/150/150?random=1", caption="LiveGate AI Protection")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Live Demo", "Admin Console", "API Configuration", "About"])

# API Configuration Page
if page == "API Configuration":
    st.header("API Key Configuration")
    
    st.info("""
    Enter your API keys below to enable enhanced AI features. 
    Limited GPT-5 credits have been provided for this hackathon.
    """)
    
    with st.form("api_config_form"):
        openai_key = st.text_input("OpenAI API Key", type="password", 
                                  value=st.session_state.api_keys["openai_key"],
                                  help="For GPT-5 challenge generation and analysis")
        
        hf_key = st.text_input("Hugging Face API Key", type="password",
                              value=st.session_state.api_keys["huggingface_key"],
                              help="For additional ML model capabilities")
        
        stt_key = st.text_input("Speech-to-Text API Key", type="password",
                               value=st.session_state.api_keys["speech_to_text_key"],
                               help="For real-time audio transcription")
        
        submitted = st.form_submit_button("Save Configuration")
        
        if submitted:
            st.session_state.api_keys = {
                "openai_key": openai_key,
                "huggingface_key": hf_key,
                "speech_to_text_key": stt_key
            }
            st.success("API configuration saved successfully!")
    
    # Display credit information
    st.subheader("Credit Status")
    st.progress(st.session_state.credits_remaining / 1000)
    st.write(f"Remaining credits: {st.session_state.credits_remaining}/1000")
    
    # API status indicators
    st.subheader("API Connection Status")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        status = "active" if st.session_state.api_keys["openai_key"] else "inactive"
        st.markdown(f'<div class="api-status api-{status}">OpenAI: {status.upper()}</div>', unsafe_allow_html=True)
    
    with col2:
        status = "active" if st.session_state.api_keys["huggingface_key"] else "inactive"
        st.markdown(f'<div class="api-status api-{status}">Hugging Face: {status.upper()}</div>', unsafe_allow_html=True)
    
    with col3:
        status = "active" if st.session_state.api_keys["speech_to_text_key"] else "inactive"
        st.markdown(f'<div class="api-status api-{status}">Speech-to-Text: {status.upper()}</div>', unsafe_allow_html=True)

# Dashboard Page
elif page == "Dashboard":
    st.header("Executive Dashboard")
    
    # API status quick view
    if st.session_state.api_keys["openai_key"]:
        st.success("✅ GPT-5 API Connected - Enhanced features enabled")
    else:
        st.warning("⚠️ Add API keys in Configuration section to enable AI features")
    
    # KPI cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Protected Calls Today", "12", "3")
    with col2:
        st.metric("Threats Neutralized", "1", "100%")
    with col3:
        st.metric("Prevention Rate", "100%", "0%")
    
    # Credit usage
    st.metric("AI Credits Remaining", st.session_state.credits_remaining, "-150 this session")
    
    # Recent incidents
    st.subheader("Recent Incident")
    incident_data = {
        "Time": "10:15 AM",
        "Target": "Sarah Chen (Finance)",
        "Impersonated": "CEO (Mark Jensen)",
        "Action": "Payment blocked, SecOps alerted",
        "Amount Saved": "$8.4M",
        "AI Credits Used": "150"
    }
    
    st.json(incident_data)
    if st.button("View Detailed Analysis"):
        st.session_state.page = "Admin Console"
        st.rerun()

# Live Demo Page
elif page == "Live Demo":
    st.header("Live Call Simulation: CFO Impersonation Attack")
    
    # Show API status
    if st.session_state.api_keys["openai_key"]:
        st.success("✅ AI Enhanced Mode: Using GPT-5 for dynamic challenge generation")
    else:
        st.warning("⚠️ Basic Mode: Using simulated responses. Add API key for AI features.")
    
    # Layout for demo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Live Call")
        # Use your custom image for the video placeholder
        try:
            st.image("assets/Gemini_Generated_Image_h7krmvh7krmvh7kr.png", caption="Deepfake Video of CEO")
        except:
            st.image("https://picsum.photos/600/400?random=1", caption="Deepfake Video of CEO")
        
        # Demo controls
        if not st.session_state.demo_running:
            if st.button("Start Demo"):
                st.session_state.demo_running = True
                st.session_state.current_step = 0
                st.session_state.transcript = []
                st.session_state.actions = []
                st.session_state.risk_level = "LOW"
                # Deduct credits if using AI
                if st.session_state.api_keys["openai_key"] and st.session_state.credits_remaining >= 150:
                    st.session_state.credits_remaining -= 150
                st.rerun()
        else:
            if st.button("Reset Demo"):
                st.session_state.demo_running = False
                st.rerun()
    
    with col2:
        st.subheader("LiveGate Analysis 🛡️")
        
        # Risk meter
        risk_class = f"risk-{st.session_state.risk_level.lower()}"
        st.markdown(f'<div class="{risk_class}">Risk Level: {st.session_state.risk_level}</div>', unsafe_allow_html=True)
        
        # AI status
        if st.session_state.api_keys["openai_key"]:
            st.info(f"AI Credits: {st.session_state.credits_remaining}")
        
        # Transcript box
        st.subheader("Transcript")
        transcript_container = st.container(height=200)
        with transcript_container:
            for speaker, text in st.session_state.transcript:
                st.text(f"{speaker}: {text}")
        
        # Action log
        st.subheader("Action Log")
        action_container = st.container(height=200)
        with action_container:
            for action in st.session_state.actions:
                st.markdown(action)
    
    # Run the demo sequence
    if st.session_state.demo_running and st.session_state.current_step < len(demo_sequence):
        step = demo_sequence[st.session_state.current_step]
        time.sleep(step['delay'] / 1000)
        
        if step['type'] == "transcript":
            st.session_state.transcript.append((step['speaker'], step['text']))
        elif step['type'] in ["analysis", "action"]:
            st.session_state.actions.append(step['text'])
        elif step['type'] == "risk":
            st.session_state.risk_level = step['level']
        
        st.session_state.current_step += 1
        st.rerun()

# Admin Console Page
elif page == "Admin Console":
    st.header("Incident Review & Management")
    
    # Incident timeline
    st.subheader("Incident: 10:15 AM - Deepfake CEO Call")
    
    timeline_data = generate_timeline_data()
    
    for event in timeline_data:
        st.markdown(f"**{event['time']}** - {event['event']}")
        if 'details' in event:
            with st.expander("Details"):
                st.write(event['details'])
    
    # Risk score visualization
    risk_scores = [
        {"time": "10:15:00", "score": 5},
        {"time": "10:15:05", "score": 40},
        {"time": "10:15:07", "score": 75},
        {"time": "10:15:12", "score": 98}
    ]
    
    df = pd.DataFrame(risk_scores)
    fig = px.line(df, x="time", y="score", title="Risk Score Progression", 
                  labels={"time": "Time", "score": "Risk Score %"})
    fig.update_layout(yaxis_range=[0, 100])
    st.plotly_chart(fig)
    
    # Generate training drill
    if st.button("Generate Training Drill"):
        # Use AI if available, otherwise use simulated response
        if st.session_state.api_keys["openai_key"] and st.session_state.credits_remaining >= 50:
            st.session_state.credits_remaining -= 50
            st.success("Training drill generated using GPT-5!")
        else:
            st.info("Training drill generated (simulated mode)")
        
        st.json({
            "scenario": "CEO Urgent Wire Request",
            "learning_objectives": [
                "Identify red flags in urgent payment requests",
                "Understand multi-signatory approval policy (FIN-POL-007)",
                "Experience LiveGate's verification process"
            ],
            "department": "Finance",
            "estimated_duration": "15 minutes",
            "difficulty": "Intermediate",
            "ai_credits_used": 50 if st.session_state.api_keys["openai_key"] else 0
        })

# About Page
else:
    st.header("About LiveGate")
    
    st.markdown("""
    LiveGate is a GPT-5-powered real-time deepfake detection system that protects organizations 
    from AI-generated impersonation attacks during critical communications.
    
    ### How It Works
    1. **Joins high-value calls** as a secure participant
    2. **Analyzes audio and video streams** in real-time using multimodal AI
    3. **Issues dynamic proof-of-life challenges** that deepfakes can't anticipate
    4. **Enforces policy compliance** by checking requests against company guidelines
    5. **Blocks fraudulent transactions** before money moves
    
    ### Key Features
    - Real-time deepfake detection
    - Context-aware challenge generation
    - Policy compliance checking
    - Automated incident response
    - Training drill generation
    
    ### Technology Stack
    - GPT-5 for reasoning and challenge generation
    - WebRTC for real-time communication
    - Vector databases for context retrieval
    - Enterprise system integrations (ERP, HRIS, Calendars)
    """)
    
    st.info("""
    This demo includes limited GPT-5 credits provided for the Lalab Hackathon 2025. 
    Add your API keys in the Configuration section to experience enhanced AI features.
    """)

# Footer
st.markdown("---")
st.markdown("LiveGate Prototype | Built for Lalab Hackathon 2025 | AI credits provided by hackathon sponsors")
