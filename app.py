import streamlit as st
import pandas as pd
import plotly.express as px
import time
from datetime import datetime

# Demo data moved into main file
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

# Header
st.markdown('<h1 class="main-header">🛡️ LiveGate</h1>', unsafe_allow_html=True)
st.markdown("**Real-Time Deepfake & Fraud Gatekeeper**")

# Sidebar
st.sidebar.image("https://picsum.photos/150/150?random=1", caption="LiveGate AI Protection")
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Live Demo", "Admin Console", "About"])

# Dashboard Page
if page == "Dashboard":
    st.header("Executive Dashboard")
    
    # KPI cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Protected Calls Today", "12", "3")
    with col2:
        st.metric("Threats Neutralized", "1", "100%")
    with col3:
        st.metric("Prevention Rate", "100%", "0%")
    
    # Recent incidents
    st.subheader("Recent Incident")
    incident_data = {
        "Time": "10:15 AM",
        "Target": "Sarah Chen (Finance)",
        "Impersonated": "CEO (Mark Jensen)",
        "Action": "Payment blocked, SecOps alerted",
        "Amount Saved": "$8.4M"
    }
    
    st.json(incident_data)
    if st.button("View Detailed Analysis"):
        st.session_state.page = "Admin Console"
        st.rerun()

# Live Demo Page
elif page == "Live Demo":
    st.header("Live Call Simulation: CFO Impersonation Attack")
    
    # Layout for demo
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Live Call")
        # Placeholder for video
        st.image("https://picsum.photos/600/400?random=1", caption="Deepfake Video of CEO")
        
        # Demo controls
        if not st.session_state.demo_running:
            if st.button("Start Demo"):
                st.session_state.demo_running = True
                st.session_state.current_step = 0
                st.session_state.transcript = []
                st.session_state.actions = []
                st.session_state.risk_level = "LOW"
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
        st.success("Training drill generated successfully!")
        st.json({
            "scenario": "CEO Urgent Wire Request",
            "learning_objectives": [
                "Identify red flags in urgent payment requests",
                "Understand multi-signatory approval policy (FIN-POL-007)",
                "Experience LiveGate's verification process"
            ],
            "department": "Finance",
            "estimated_duration": "15 minutes",
            "difficulty": "Intermediate"
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
    
    st.info("This is a prototype demonstration for hackathon purposes.")

# Footer
st.markdown("---")
st.markdown("LiveGate Prototype | Built for Lalab Hackathon 2025")
