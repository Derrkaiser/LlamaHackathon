import streamlit as st
import os
import asyncio
from pathlib import Path
import tempfile
import shutil

# Page configuration
st.set_page_config(
    page_title="Llama Hackathon Demo Generator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .sub-header {
        font-size: 1.5rem;
        color: #4a5568;
        margin-bottom: 1rem;
        font-weight: 600;
    }
    
    .info-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    
    .form-container {
        background: #f8fafc;
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #667eea;
    }
    
    .metric-label {
        color: #718096;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<h1 class="main-header">🚀 Llama Hackathon Demo Generator</h1>', unsafe_allow_html=True)
    
    # Info box
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Generate AI-Powered Presentations</h3>
        <p>Upload your requirements, connect your GitHub repo, and let Llama 4 Maverick create a synchronized presentation with Tavus avatar and live demo orchestration.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Main form container
    with st.container():
        st.markdown('<div class="form-container">', unsafe_allow_html=True)
        
        # Two columns for better layout
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 class="sub-header">📁 Project Information</h3>', unsafe_allow_html=True)
            
            # GitHub Repository URL
            github_url = st.text_input(
                "GitHub Repository URL",
                placeholder="https://github.com/username/repository",
                help="Enter the full GitHub repository URL for codebase analysis"
            )
            
            # Requirements PDF Upload
            st.markdown('<h4 style="margin-top: 2rem;">📄 Requirements Document</h4>', unsafe_allow_html=True)
            
            uploaded_file = st.file_uploader(
                "Upload Requirements PDF",
                type=['pdf'],
                help="Upload your requirements document (PDF format)"
            )
            
            # Alternative: PDF file path
            pdf_path = st.text_input(
                "Or provide PDF file path",
                placeholder="/path/to/requirements.pdf",
                help="Alternative: provide the file path to your requirements PDF"
            )
            
            # Demo Duration
            demo_duration = st.selectbox(
                "Demo Duration",
                options=[3, 5, 7, 10, 15],
                index=1,  # Default to 5 minutes
                help="Select the desired duration for your demo presentation"
            )
        
        with col2:
            st.markdown('<h3 class="sub-header">🎭 Presentation Details</h3>', unsafe_allow_html=True)
            
            # Audience Type
            audience_type = st.selectbox(
                "Target Audience",
                options=[
                    "Technical Developers",
                    "Product Managers",
                    "Business Stakeholders",
                    "Mixed Technical & Business",
                    "Investors",
                    "End Users",
                    "Custom"
                ],
                help="Select the primary audience for your presentation"
            )
            
            # Custom audience description
            if audience_type == "Custom":
                custom_audience = st.text_area(
                    "Describe your audience",
                    placeholder="Describe the technical level, roles, and interests of your audience...",
                    height=100
                )
            else:
                custom_audience = ""
            
            # Demo Purpose
            demo_purpose = st.selectbox(
                "Demo Purpose",
                options=[
                    "Feature Showcase",
                    "Technical Deep Dive",
                    "Product Launch",
                    "Investor Pitch",
                    "User Onboarding",
                    "Bug Fix Demonstration",
                    "Architecture Review",
                    "Custom"
                ],
                help="What is the main goal of this demo?"
            )
            
            # Custom purpose description
            if demo_purpose == "Custom":
                custom_purpose = st.text_area(
                    "Describe your demo purpose",
                    placeholder="Explain the specific goals and outcomes you want from this demo...",
                    height=100
                )
            else:
                custom_purpose = ""
            
            # Focus Areas
            st.markdown('<h4 style="margin-top: 1rem;">🎯 Focus Areas</h4>', unsafe_allow_html=True)
            
            focus_areas = st.multiselect(
                "What should the demo emphasize?",
                options=[
                    "User Interface & UX",
                    "Backend Architecture",
                    "Database Design",
                    "API Integration",
                    "Security Features",
                    "Performance Optimization",
                    "Scalability",
                    "Mobile Responsiveness",
                    "Real-time Features",
                    "Data Analytics",
                    "Authentication & Authorization",
                    "File Management",
                    "Search Functionality",
                    "Custom"
                ],
                default=["User Interface & UX", "Backend Architecture"],
                help="Select the key areas you want to highlight in the demo"
            )
            
            if "Custom" in focus_areas:
                custom_focus = st.text_area(
                    "Describe custom focus areas",
                    placeholder="Describe any specific features or aspects you want to emphasize...",
                    height=80
                )
            else:
                custom_focus = ""
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Additional Configuration
    with st.expander("⚙️ Advanced Configuration", expanded=False):
        col3, col4 = st.columns(2)
        
        with col3:
            st.markdown('<h4>🤖 Llama Configuration</h4>', unsafe_allow_html=True)
            
            # Llama API Key
            llama_api_key = st.text_input(
                "Llama API Key",
                type="password",
                help="Your Llama API key for generating content"
            )
            
            # Model selection
            llama_model = st.selectbox(
                "Llama Model",
                options=["Llama-4-Maverick-17B-128E-Instruct-FP8"],
                help="Select the Llama model to use"
            )
        
        with col4:
            st.markdown('<h4>🎬 Demo Configuration</h4>', unsafe_allow_html=True)
            
            # Demo URL
            demo_url = st.text_input(
                "Demo URL (optional)",
                placeholder="http://localhost:3000",
                help="If you know the demo URL, provide it here. Otherwise, we'll try to discover it."
            )
            
            # Include code analysis
            include_code_analysis = st.checkbox(
                "Include detailed code analysis",
                value=True,
                help="Generate detailed insights about the codebase architecture and implementation"
            )
            
            # Include risk assessment
            include_risk_assessment = st.checkbox(
                "Include demo risk assessment",
                value=True,
                help="Identify potential demo risks and prepare fallback scenarios"
            )
    
    # Metrics row
    st.markdown('<h3 style="margin: 2rem 0 1rem 0;">📊 Project Overview</h3>', unsafe_allow_html=True)
    
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">🚀</div>
            <div class="metric-label">Demo Generator</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">🤖</div>
            <div class="metric-label">Llama 4 Maverick</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">🎭</div>
            <div class="metric-label">Tavus Avatar</div>
        </div>
        """, unsafe_allow_html=True)
    
    with metric_col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">⚡</div>
            <div class="metric-label">Live Demo</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Generate button
    st.markdown('<div style="text-align: center; margin: 3rem 0;">', unsafe_allow_html=True)
    
    if st.button("🚀 Generate AI Presentation", type="primary", use_container_width=True):
        # Validate inputs
        if not github_url and not (uploaded_file or pdf_path):
            st.error("Please provide either a GitHub repository URL or a requirements document.")
            return
        
        if not llama_api_key:
            st.error("Please provide your Llama API key.")
            return
        
        # Show processing
        with st.spinner("🤖 Analyzing your project and generating presentation..."):
            try:
                # Import and use the integration
                from ui_integration import process_demo_request
                
                # Prepare inputs
                ui_inputs = {
                    "github_url": github_url,
                    "uploaded_file": uploaded_file,
                    "pdf_path": pdf_path,
                    "demo_duration": demo_duration,
                    "audience_type": audience_type,
                    "custom_audience": custom_audience,
                    "demo_purpose": demo_purpose,
                    "custom_purpose": custom_purpose,
                    "focus_areas": focus_areas,
                    "custom_focus": custom_focus,
                    "llama_api_key": llama_api_key,
                    "demo_url": demo_url,
                    "include_code_analysis": include_code_analysis,
                    "include_risk_assessment": include_risk_assessment
                }
                
                # Process the request
                result = asyncio.run(process_demo_request(ui_inputs))
                
                st.success("✅ Analysis complete! Presentation script and demo plan generated.")
                
                # Show results in tabs
                tab1, tab2, tab3 = st.tabs(["📝 Presentation Script", "🎬 Demo Plan", "📊 Analysis Summary"])
                
                with tab1:
                    st.markdown("### Generated Presentation Script")
                    if isinstance(result["presentation_script"], dict):
                        # If it's a structured response, show the content
                        if "sections" in result["presentation_script"]:
                            for section in result["presentation_script"]["sections"]:
                                st.markdown(f"**{section.get('title', 'Section')}** ({section.get('duration', 0)}s)")
                                st.text(section.get('content', 'No content'))
                                st.markdown("---")
                        else:
                            st.json(result["presentation_script"])
                    else:
                        # If it's a string response, show as code
                        st.code(result["presentation_script"])
                
                with tab2:
                    st.markdown("### Demo Execution Plan")
                    st.json(result["agent_execution_plan"])
                
                with tab3:
                    st.markdown("### Analysis Summary")
                    col_summary1, col_summary2 = st.columns(2)
                    
                    with col_summary1:
                        st.metric("Requirements Found", result["analysis_summary"]["requirements_count"])
                        st.metric("Key Features", result["analysis_summary"]["features_count"])
                        st.metric("Demo Duration", f"{demo_duration} min")
                    
                    with col_summary2:
                        st.metric("Code Complexity", result["analysis_summary"]["complexity"])
                        st.metric("Risk Level", result["analysis_summary"]["risk_level"])
                        st.metric("Visual Assets", "3")
                    
                    # Show detailed summary
                    st.markdown("### Detailed Analysis")
                    st.text(result["analysis_summary"]["summary"])
                
            except Exception as e:
                st.error(f"❌ Processing failed: {str(e)}")
                st.info("💡 Make sure your Llama API key is correct and you have sufficient credits.")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #718096; margin-top: 2rem;">
        <p>Built with ❤️ for the Llama Hackathon | Powered by Llama 4 Maverick & Tavus</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 