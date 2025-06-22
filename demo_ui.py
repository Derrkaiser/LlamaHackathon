import streamlit as st
import os
import asyncio
from pathlib import Path
import tempfile
import shutil
import time

# Page configuration
st.set_page_config(
    page_title="DemoAM",
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
    st.markdown('<h1 class="main-header">DemoAM</h1>', unsafe_allow_html=True)
    
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
                options=[1],
                index=0,  # Default to 1 minute to conserve Tavus credits
                help="Set to 1 minute to conserve Tavus API credits"
            )
            st.info("⚠️ Limited to 1 minute to conserve Tavus API credits")
        
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
        
        # Show processing with detailed progress
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Initialize
            status_text.text("🔧 Initializing processing pipeline...")
            progress_bar.progress(10)
            
            # Step 2: GitHub Analysis (if provided)
            if github_url:
                status_text.text(f"🔍 Analyzing GitHub repository: {github_url}")
                progress_bar.progress(20)
            
            # Step 3: PDF Processing (if provided)
            if uploaded_file or pdf_path:
                status_text.text("📄 Parsing requirements document...")
                progress_bar.progress(40)
            
            # Step 4: Context Building
            status_text.text("🧠 Building comprehensive context...")
            progress_bar.progress(60)
            
            # Step 5: Llama Processing
            status_text.text("🤖 Generating presentation with Llama 4 Maverick...")
            progress_bar.progress(80)
            
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
            
            # Store avatar video URL in session state for persistence
            if result.get("avatar_video_url"):
                # Initialize video history if it doesn't exist
                if 'avatar_video_history' not in st.session_state:
                    st.session_state.avatar_video_history = []
                
                # Add new video to history
                new_video = {
                    "url": result.get("avatar_video_url", ""),
                    "status": result.get("avatar_status", "unknown"),
                    "presentation_id": result.get("avatar_presentation_id", ""),
                    "timestamp": "Just generated",
                    "script_preview": result.get("presentation_script", "")[:200] + "..." if len(result.get("presentation_script", "")) > 200 else result.get("presentation_script", ""),
                    "needs_status_check": True  # Flag to check status later
                }
                
                st.session_state.avatar_video_history.append(new_video)
                
                # Keep only last 5 videos
                if len(st.session_state.avatar_video_history) > 5:
                    st.session_state.avatar_video_history = st.session_state.avatar_video_history[-5:]
                
                # Set current video as the latest
                st.session_state.avatar_video_url = result.get("avatar_video_url")
                st.session_state.avatar_status = result.get("avatar_status", "unknown")
                st.session_state.avatar_presentation_id = result.get("avatar_presentation_id", "")
            
            # Store demo results in session state for persistence
            st.session_state.demo_results = result
            
            # Complete
            status_text.text("✅ Analysis complete!")
            progress_bar.progress(100)
            
            st.success("🎉 Presentation script and demo plan generated successfully!")
            
            # Show results in tabs
            tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Presentation Script", "🎬 Demo Plan", "📊 Analysis Summary", "🔍 Raw Context", "🎭 Live Tavus Avatar"])
            
            with tab1:
                st.markdown("### Generated Presentation Script")
                if isinstance(result["presentation_script"], dict):
                    # If it's a structured response, show the content
                    if "presentation_script" in result["presentation_script"]:
                        script = result["presentation_script"]["presentation_script"]
                        if "sections" in script:
                            for i, section in enumerate(script["sections"], 1):
                                with st.expander(f"Section {i}: {section.get('title', 'Untitled')} ({section.get('duration', 0)}s)", expanded=i==1):
                                    st.markdown(section.get('content', 'No content'))
                                    if section.get('demo_steps'):
                                        st.markdown("**Demo Steps:**")
                                        for step in section['demo_steps']:
                                            st.markdown(f"- {step}")
                        else:
                            st.json(script)
                    else:
                        st.json(result["presentation_script"])
                else:
                    # If it's a string response, show as code
                    st.code(result["presentation_script"])
                
                # Download button for presentation script
                if st.button("📥 Download Presentation Script"):
                    import json
                    script_json = json.dumps(result["presentation_script"], indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=script_json,
                        file_name="presentation_script.json",
                        mime="application/json"
                    )
            
            with tab2:
                st.markdown("### Demo Execution Plan")
                st.json(result["agent_execution_plan"])
                
                # Download button for demo plan
                if st.button("📥 Download Demo Plan"):
                    import json
                    plan_json = json.dumps(result["agent_execution_plan"], indent=2)
                    st.download_button(
                        label="Download JSON",
                        data=plan_json,
                        file_name="demo_plan.json",
                        mime="application/json"
                    )
            
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
                    st.metric("Presentation Duration", f"{result['analysis_summary'].get('presentation_duration', 0)}s")
                
                # Show detailed summary
                st.markdown("### Detailed Analysis")
                st.text(result["analysis_summary"]["summary"])
                
                # Show codebase and document context
                if "codebase_context" in result:
                    st.markdown("### Codebase Context")
                    st.json(result["codebase_context"])
                
                if "document_context" in result:
                    st.markdown("### Document Context")
                    st.json(result["document_context"])
            
            with tab4:
                st.markdown("### Raw Processing Context")
                st.markdown("This shows the raw context that was sent to Llama for processing.")
                
                # Show what was processed
                context_info = {
                    "GitHub URL": github_url or "None provided",
                    "PDF Document": uploaded_file.name if uploaded_file else (pdf_path or "None provided"),
                    "Audience": audience_type,
                    "Purpose": demo_purpose,
                    "Duration": f"{demo_duration} minutes",
                    "Focus Areas": focus_areas,
                    "Code Analysis": "Enabled" if include_code_analysis else "Disabled",
                    "Risk Assessment": "Enabled" if include_risk_assessment else "Disabled"
                }
                
                st.json(context_info)
                
            with tab5:
                st.markdown("### 🎭 Live Tavus Avatar Presentation")
                
                # Status checking function
                def check_video_status():
                    """Check status of videos that need updating"""
                    if 'avatar_video_history' in st.session_state:
                        for video in st.session_state.avatar_video_history:
                            if video.get('needs_status_check') and video.get('presentation_id'):
                                try:
                                    # Import Tavus client to check status
                                    from src.core.tavus_client import TavusClient
                                    tavus_client = TavusClient()
                                    status_data = tavus_client.get_video_status(video['presentation_id'])
                                    
                                    if status_data.get('status') == 'ready':
                                        video['status'] = 'completed'
                                        video['needs_status_check'] = False
                                        video['url'] = status_data.get('hosted_url', video.get('url', ''))
                                        st.success(f"✅ Video {video['presentation_id']} is ready!")
                                    elif status_data.get('status') in ['queued', 'generating']:
                                        video['status'] = status_data.get('status')
                                        st.info(f"⏳ Video {video['presentation_id']} is still processing...")
                                    else:
                                        video['status'] = status_data.get('status', 'unknown')
                                        video['needs_status_check'] = False
                                except Exception as e:
                                    st.warning(f"Could not check status for video {video['presentation_id']}: {str(e)}")
                
                # Check for videos that need status updates
                if st.button("🔄 Check All Video Status"):
                    check_video_status()
                    st.rerun()
                
                # Check if we have video history
                video_history = st.session_state.get("avatar_video_history", [])
                
                if video_history:
                    st.success(f"✅ Found {len(video_history)} generated videos!")
                    
                    # Video selector
                    if len(video_history) > 1:
                        st.subheader("📺 Select Video to View")
                        video_options = [f"Video {i+1}: {video.get('presentation_id', 'Unknown')} - {video.get('timestamp', 'Unknown')}" for i, video in enumerate(video_history)]
                        selected_video_index = st.selectbox("Choose a video:", range(len(video_history)), format_func=lambda x: video_options[x])
                        selected_video = video_history[selected_video_index]
                    else:
                        selected_video = video_history[0]
                    
                    # Display selected video
                    st.subheader(f"🎬 Video: {selected_video.get('presentation_id', 'Unknown')}")
                    
                    # Show video info
                    col_info1, col_info2, col_info3 = st.columns(3)
                    with col_info1:
                        st.metric("Presentation ID", selected_video.get('presentation_id', 'N/A'))
                    with col_info2:
                        st.metric("Status", selected_video.get('status', 'Unknown'))
                    with col_info3:
                        st.metric("Video Ready", "✅ Yes")
                    
                    # Display the video
                    st.markdown("### 🎬 Your Avatar Presentation")
                    
                    # Show direct links
                    st.markdown("### 🔗 Direct Links")
                    col_link1, col_link2, col_link3 = st.columns(3)
                    
                    with col_link1:
                        st.link_button("🔗 Open in Tavus", selected_video.get('url', ''))
                    
                    with col_link2:
                        presentation_id = selected_video.get('presentation_id', '')
                        if presentation_id:
                            st.link_button("👁️ View in App", f"https://app.tavus.com/video/{presentation_id}")
                    
                    with col_link3:
                        st.link_button("📺 Embed URL", f"https://app.tavus.com/embed/{presentation_id}")
                    
                    # Show script preview
                    with st.expander("📝 Script Preview"):
                        script_preview = selected_video.get('script_preview', 'No preview available')
                        st.text_area("Generated Script", value=script_preview, height=200, disabled=True)
                    
                    # Show video history
                    if len(video_history) > 1:
                        with st.expander("📚 Video History"):
                            st.markdown("### Previously Generated Videos")
                            for i, video in enumerate(video_history):
                                st.markdown(f"**Video {i+1}:** {video.get('presentation_id', 'Unknown')} - {video.get('timestamp', 'Unknown')}")
                                st.markdown(f"   URL: {video.get('url', 'No URL')}")
                                st.markdown("---")
                
                else:
                    # Use session state if available, otherwise use current result
                    avatar_status = st.session_state.get("avatar_status", result.get("avatar_status", "unknown"))
                    avatar_video_url = st.session_state.get("avatar_video_url", result.get("avatar_video_url", ""))
                    avatar_presentation_id = st.session_state.get("avatar_presentation_id", result.get("avatar_presentation_id", ""))
                    
                    if avatar_status == "completed" and avatar_video_url:
                        st.success("✅ Tavus avatar created successfully!")
                        
                        # Show avatar info
                        col_info1, col_info2, col_info3 = st.columns(3)
                        with col_info1:
                            st.metric("Presentation ID", avatar_presentation_id or "N/A")
                        with col_info2:
                            st.metric("Status", avatar_status)
                        with col_info3:
                            st.metric("Video Ready", "✅ Yes")
                        
                        # Display the video
                        st.markdown("### 🎬 Your Avatar Presentation")
                        
                        # Show direct links
                        st.markdown("### 🔗 Direct Links")
                        col_link1, col_link2, col_link3 = st.columns(3)
                        
                        with col_link1:
                            st.link_button("🔗 Open in Tavus", f"https://tavus.video/{avatar_presentation_id}")
                        
                        with col_link2:
                            st.link_button("👁️ View in App", f"https://app.tavus.com/video/{avatar_presentation_id}")
                        
                        with col_link3:
                            st.link_button("📺 Embed URL", f"https://app.tavus.com/embed/{avatar_presentation_id}")
                        
                        # Show script preview
                        with st.expander("📝 Script Preview"):
                            script_preview = result.get("presentation_script", "")[:500] + "..." if len(result.get("presentation_script", "")) > 500 else result.get("presentation_script", "")
                            st.text_area("Generated Script", value=script_preview, height=200, disabled=True)
                    
                    elif avatar_status == "failed":
                        st.error(f"❌ Avatar creation failed")
                        st.info("💡 The script was generated successfully, but the avatar creation failed. You can still use the script for manual presentation.")
                    
                    else:
                        st.info("🎭 Avatar presentation will appear here when demo is generated")
                        
                        # Show the existing calculator video
                        st.subheader("🎬 Calculator App Demo")
                        
                        # Show direct links
                        st.markdown("### 🔗 Direct Links")
                        col_link1, col_link2, col_link3 = st.columns(3)
                        
                        with col_link1:
                            st.link_button("🔗 Open in Tavus", "https://tavus.video/f6898a5b37")
                        
                        with col_link2:
                            st.link_button("👁️ View in App", "https://app.tavus.com/video/f6898a5b37")
                        
                        with col_link3:
                            st.link_button("📺 Embed URL", "https://app.tavus.com/embed/f6898a5b37")
                        
                        # Show script preview
                        with st.expander("📝 Script Preview"):
                            script_preview = "Calculator app presentation with microservices architecture, React frontend, Python backend, and key features including Calculator Display Component, Numeric & Operator Buttons, Arithmetic Computation Engine, and Clear & All-Clear Functionality."
                            st.text_area("Generated Script", value=script_preview, height=200, disabled=True)
                        
                        # Show sample avatar info
                        st.markdown("""
                        ### 🎭 Tavus Avatar Features
                        
                        Your avatar will:
                        - 📖 Read the generated script naturally with AI voice
                        - ⏸️ Pause at appropriate moments for emphasis
                        - 👋 Use realistic gestures and expressions
                        - 🎯 Adapt tone and pace for your audience
                        - ⏱️ Follow the timing you specified (1 minute)
                        - 🎨 Use professional presentation styling
                        
                        **To see the avatar in action:**
                        1. Generate a demo above with your GitHub repo and requirements
                        2. Wait for the Tavus API to create your avatar
                        3. The avatar will appear here automatically
                        """)
        
        except Exception as e:
            st.error(f"❌ Processing failed: {str(e)}")
            st.info("💡 Troubleshooting tips:")
            st.markdown("""
            - Make sure your Llama API key is correct and has sufficient credits
            - Check that the GitHub URL is valid and accessible
            - Ensure the PDF file is not corrupted and is readable
            - Try reducing the demo duration or focus areas if the request is too complex
            """)
            
            # Show detailed error for debugging
            with st.expander("🔍 Debug Information"):
                st.code(str(e))
        
        finally:
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #718096; margin-top: 2rem;">
        <p>Built with ❤️ for the Llama Hackathon | Powered by Llama 4 Maverick & Tavus</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Always show results tabs
    st.markdown("---")
    st.header("🎬 Demo Results")
    
    # Auto-refresh for video status using Streamlit's mechanism
    if 'avatar_video_history' in st.session_state and st.session_state.avatar_video_history:
        # Check if any videos are still processing
        processing_videos = [v for v in st.session_state.avatar_video_history if v.get('status') in ['queued', 'generating']]
        if processing_videos:
            st.info("🔄 Videos are still processing... Refresh the page to check status")
            # Add a refresh button
            if st.button("🔄 Check Video Status"):
                st.rerun()
    
    # Show results in tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📝 Presentation Script", "🎬 Demo Plan", "📊 Analysis Summary", "🔍 Raw Context", "🎭 Live Tavus Avatar"])
    
    # Get results from session state or use empty defaults
    result = st.session_state.get('demo_results', {})
    
    with tab1:
        st.markdown("### Generated Presentation Script")
        presentation_script = result.get("presentation_script", "No script generated yet")
        if isinstance(presentation_script, str):
            st.code(presentation_script)
        else:
            st.json(presentation_script)
    
    with tab2:
        st.markdown("### Demo Execution Plan")
        demo_plan = result.get("agent_execution_plan", {})
        st.json(demo_plan)
    
    with tab3:
        st.markdown("### Analysis Summary")
        analysis_summary = result.get("analysis_summary", {})
        if analysis_summary:
            col_summary1, col_summary2 = st.columns(2)
            with col_summary1:
                st.metric("Requirements Found", analysis_summary.get("requirements_count", 0))
                st.metric("Key Features", analysis_summary.get("features_count", 0))
            with col_summary2:
                st.metric("Code Complexity", analysis_summary.get("complexity", "Unknown"))
                st.metric("Risk Level", analysis_summary.get("risk_level", "Unknown"))
        else:
            st.info("No analysis summary available")
    
    with tab4:
        st.markdown("### Raw Processing Context")
        st.info("Raw context will appear here after demo generation")
    
    with tab5:
        st.markdown("### 🎭 Live Tavus Avatar Presentation")
        
        # Use session state for avatar data
        avatar_status = st.session_state.get("avatar_status", "unknown")
        avatar_video_url = st.session_state.get("avatar_video_url", "")
        avatar_presentation_id = st.session_state.get("avatar_presentation_id", "")
        
        if avatar_status == "completed" and avatar_video_url:
            st.success("✅ Tavus avatar created successfully!")
            
            # Show avatar info
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.metric("Presentation ID", avatar_presentation_id or "N/A")
            with col_info2:
                st.metric("Status", avatar_status)
            with col_info3:
                st.metric("Video Ready", "✅ Yes")
            
            # Display the video
            st.markdown("### 🎬 Your Avatar Presentation")
            
            # Show direct links
            st.markdown("### 🔗 Direct Links")
            col_link1, col_link2, col_link3 = st.columns(3)
            
            with col_link1:
                st.link_button("🔗 Open in Tavus", f"https://tavus.video/{avatar_presentation_id}")
            
            with col_link2:
                st.link_button("👁️ View in App", f"https://app.tavus.com/video/{avatar_presentation_id}")
            
            with col_link3:
                st.link_button("📺 Embed URL", f"https://app.tavus.com/embed/{avatar_presentation_id}")
            
            # Show script preview
            with st.expander("📝 Script Preview"):
                script_preview = result.get("presentation_script", "")[:500] + "..." if len(result.get("presentation_script", "")) > 500 else result.get("presentation_script", "")
                st.text_area("Generated Script", value=script_preview, height=200, disabled=True)
        
        elif avatar_status == "failed":
            st.error(f"❌ Avatar creation failed")
            st.info("💡 The script was generated successfully, but the avatar creation failed. You can still use the script for manual presentation.")
        
        else:
            st.info("🎭 Avatar presentation will appear here when demo is generated")
            
            # Show the existing calculator video
            st.subheader("🎬 Calculator App Demo")
            
            # Show direct links
            st.markdown("### 🔗 Direct Links")
            col_link1, col_link2, col_link3 = st.columns(3)
            
            with col_link1:
                st.link_button("🔗 Open in Tavus", "https://tavus.video/f6898a5b37")
            
            with col_link2:
                st.link_button("👁️ View in App", "https://app.tavus.com/video/f6898a5b37")
            
            with col_link3:
                st.link_button("📺 Embed URL", "https://app.tavus.com/embed/f6898a5b37")
            
            # Show script preview
            with st.expander("📝 Script Preview"):
                script_preview = "Calculator app presentation with microservices architecture, React frontend, Python backend, and key features including Calculator Display Component, Numeric & Operator Buttons, Arithmetic Computation Engine, and Clear & All-Clear Functionality."
                st.text_area("Generated Script", value=script_preview, height=200, disabled=True)
            
            # Show sample avatar info
            st.markdown("""
            ### 🎭 Tavus Avatar Features
            
            Your avatar will:
            - 📖 Read the generated script naturally with AI voice
            - ⏸️ Pause at appropriate moments for emphasis
            - 👋 Use realistic gestures and expressions
            - 🎯 Adapt tone and pace for your audience
            - ⏱️ Follow the timing you specified (1 minute)
            - 🎨 Use professional presentation styling
            
            **To see the avatar in action:**
            1. Generate a demo above with your GitHub repo and requirements
            2. Wait for the Tavus API to create your avatar
            3. The avatar will appear here automatically
            """)

    # Demo settings
    st.subheader("🎬 Demo Settings")
    demo_duration = st.slider("Demo Duration (minutes)", 1, 1, 1)
    st.info("⚠️ Limited to 1 minute to conserve Tavus API credits")

if __name__ == "__main__":
    main() 