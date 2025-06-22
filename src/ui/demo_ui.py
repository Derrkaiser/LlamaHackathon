#!/usr/bin/env python3
"""
Demo UI - Streamlit interface with integrated Tavus avatar presentation
"""

import streamlit as st
import json
import time
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.unified_processor import UnifiedProcessor
from core.simple_avatar_presenter import SimpleAvatarPresenter
from config import SYSTEM_PROMPT, STREAMLIT_CONFIG

# Configure Streamlit
st.set_page_config(**STREAMLIT_CONFIG)

def main():
    """Main Streamlit application"""
    
    st.title("DemoAM - AI-Powered Demo Generator")
    st.markdown("Generate compelling presentations with Tavus avatar and natural pauses")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # API Keys
        llama_api_key = st.text_input(
            "Llama API Key",
            type="password",
            help="Your Llama API key for generating scripts"
        )
        
        tavus_api_key = st.text_input(
            "Tavus API Key", 
            type="password",
            help="Your Tavus API key for avatar control"
        )
        
        # Demo settings
        st.subheader("🎬 Demo Settings")
        demo_duration = st.slider("Demo Duration (minutes)", 1, 1, 1)
        st.info("⚠️ Limited to 1 minute to conserve Tavus API credits")
        
        # Advanced settings
        with st.expander("🔧 Advanced Settings"):
            avatar_gestures = st.checkbox(
                "Enable Avatar Gestures",
                value=True,
                help="Synchronize avatar gestures with content"
            )
            
            natural_pauses = st.checkbox(
                "Enable Natural Pauses",
                value=True,
                help="Add natural pauses for better flow"
            )
            
            auto_start = st.checkbox(
                "Auto-start Presentation",
                value=False,
                help="Automatically start avatar presentation after generation"
            )
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Input")
        
        # GitHub Repository
        github_url = st.text_input(
            "GitHub Repository URL",
            placeholder="https://github.com/username/repo",
            help="Repository to analyze for demo content"
        )
        
        # Requirements Document
        uploaded_file = st.file_uploader(
            "Upload Requirements Document (PDF/DOCX)",
            type=['pdf', 'docx'],
            help="Product requirements or feature specifications"
        )
        
        # Alternative: Requirements path
        requirements_path = st.text_input(
            "Or specify requirements file path",
            placeholder="/path/to/requirements.pdf",
            help="Local path to requirements document"
        )
        
        # Audience and purpose
        col_a, col_b = st.columns(2)
        with col_a:
            audience = st.selectbox(
                "Target Audience",
                ["Technical Developers", "Product Managers", "Business Stakeholders", "Investors", "Mixed Audience"],
                index=4
            )
        
        with col_b:
            purpose = st.selectbox(
                "Demo Purpose",
                ["Feature Showcase", "Technical Deep Dive", "Business Pitch", "User Onboarding", "Competitive Analysis"],
                index=0
            )
        
        # Generate button
        if st.button("🚀 Generate Demo", type="primary", use_container_width=True):
            if not llama_api_key:
                st.error("❌ Llama API key is required")
                return
            
            if not github_url and not uploaded_file and not requirements_path:
                st.error("❌ Please provide either a GitHub URL or requirements document")
                return
            
            # Set environment variable
            os.environ["LLAMA_API_KEY"] = llama_api_key
            if tavus_api_key:
                os.environ["TAVUS_API_KEY"] = tavus_api_key
            
            # Generate demo
            with st.spinner("🤖 Generating demo with Llama 4 Maverick..."):
                try:
                    processor = UnifiedProcessor()
                    
                    # Process inputs
                    result = processor.process_demo_request(
                        github_url=github_url,
                        requirements_file=uploaded_file,
                        requirements_path=requirements_path,
                        audience=audience,
                        purpose=purpose,
                        demo_duration=demo_duration
                    )
                    
                    # Store results in session state
                    st.session_state.demo_results = result
                    st.session_state.avatar_gestures = avatar_gestures
                    st.session_state.natural_pauses = natural_pauses
                    
                    st.success("✅ Demo generated successfully!")
                    
                    # Auto-start if enabled
                    if auto_start:
                        st.session_state.auto_start_presentation = True
                    
                except Exception as e:
                    st.error(f"❌ Error generating demo: {str(e)}")
    
    with col2:
        st.header("📊 Status")
        
        # Demo status
        if 'demo_results' in st.session_state:
            st.success("✅ Demo Ready")
            
            results = st.session_state.demo_results
            st.metric("Script Length", f"{len(results.get('presentation_script', ''))} chars")
            st.metric("Demo Steps", len(results.get('demo_plan', {}).get('steps', [])))
            
            if 'avatar_script' in results:
                avatar_segments = results['avatar_script'].get('presentation', {}).get('segments', [])
                st.metric("Avatar Segments", len(avatar_segments))
                
                timing = results['avatar_script'].get('timing', {})
                st.metric("Duration", f"{timing.get('total_duration', 0):.1f}s")
                st.metric("Pauses", timing.get('pause_count', 0))
        else:
            st.info("⏳ No demo generated yet")
    
    # Results tabs
    if 'demo_results' in st.session_state:
        st.header("🎬 Demo Results")
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📝 Presentation Script", 
            "🤖 Demo Plan", 
            "🎭 Avatar Script", 
            "🎬 Live Tavus Avatar"
        ])
        
        results = st.session_state.demo_results
        
        with tab1:
            st.subheader("Generated Presentation Script")
            st.text_area(
                "Script",
                value=results.get('presentation_script', ''),
                height=400,
                disabled=True
            )
            
            # Download button
            st.download_button(
                "📥 Download Script",
                data=results.get('presentation_script', ''),
                file_name="presentation_script.txt",
                mime="text/plain"
            )
        
        with tab2:
            st.subheader("Demo Execution Plan")
            
            demo_plan = results.get('demo_plan', {})
            
            # Overview
            col_a, col_b, col_c = st.columns(3)
            with col_a:
                st.metric("Total Steps", len(demo_plan.get('steps', [])))
            with col_b:
                st.metric("Estimated Time", f"{demo_plan.get('estimated_duration', 0)} min")
            with col_c:
                st.metric("Demo URL", demo_plan.get('demo_url', 'Not specified'))
            
            # Steps
            st.subheader("Demo Steps")
            for i, step in enumerate(demo_plan.get('steps', []), 1):
                with st.expander(f"Step {i}: {step.get('action', 'Unknown')}"):
                    st.write(f"**Description:** {step.get('description', 'No description')}")
                    st.write(f"**Duration:** {step.get('duration', 0)} seconds")
                    st.write(f"**Expected Outcome:** {step.get('expected_outcome', 'Not specified')}")
        
        with tab3:
            st.subheader("Tavus Avatar Script")
            
            avatar_script = results.get('avatar_script', {})
            
            if avatar_script:
                # Avatar configuration
                avatar_config = avatar_script.get('avatar_config', {})
                st.json(avatar_config)
                
                # Presentation segments
                st.subheader("Presentation Segments")
                segments = avatar_script.get('presentation', {}).get('segments', [])
                
                for i, segment in enumerate(segments, 1):
                    with st.expander(f"Segment {i}: {segment.get('id', 'Unknown')}"):
                        st.write(f"**Text:** {segment.get('text', 'No text')}")
                        st.write(f"**Duration:** {segment.get('duration', 0)} seconds")
                        st.write(f"**Gesture:** {segment.get('gesture', 'Default')}")
                        st.write(f"**Pause After:** {'Yes' if segment.get('pause_after', False) else 'No'}")
                
                # Timing summary
                st.subheader("Timing Summary")
                timing = avatar_script.get('timing', {})
                col_t1, col_t2, col_t3 = st.columns(3)
                with col_t1:
                    st.metric("Total Duration", f"{timing.get('total_duration', 0):.1f}s")
                with col_t2:
                    st.metric("Segment Count", timing.get('segment_count', 0))
                with col_t3:
                    st.metric("Natural Pauses", timing.get('pause_count', 0))
            else:
                st.warning("No avatar script generated")
        
        with tab4:
            st.subheader("🎭 Live Tavus Avatar Presentation")
            
            avatar_script = results.get('avatar_script', {})
            
            if avatar_script and avatar_script.get('status') == 'completed':
                # Display the real Tavus avatar
                st.success("✅ Tavus avatar created successfully!")
                
                # Show avatar info
                col_info1, col_info2, col_info3 = st.columns(3)
                with col_info1:
                    st.metric("Presentation ID", avatar_script.get('presentation_id', 'N/A'))
                with col_info2:
                    st.metric("Status", avatar_script.get('status', 'Unknown'))
                with col_info3:
                    duration = avatar_script.get('duration', 0)
                    st.metric("Duration", f"{duration:.1f}s" if duration else "N/A")
                
                # Display the embed code
                embed_code = avatar_script.get('embed_code', '')
                if embed_code:
                    st.components.v1.html(embed_code, height=700)
                else:
                    st.warning("No embed code available")
                
                # Show script preview
                with st.expander("📝 Script Preview"):
                    script_preview = avatar_script.get('script_preview', 'No preview available')
                    st.text_area("Generated Script", value=script_preview, height=200, disabled=True)
                
                # Download links
                st.subheader("📥 Download Options")
                col_dl1, col_dl2 = st.columns(2)
                
                with col_dl1:
                    if avatar_script.get('embed_url'):
                        st.link_button("🔗 Open in Tavus", avatar_script['embed_url'])
                
                with col_dl2:
                    if avatar_script.get('preview_url'):
                        st.link_button("👁️ Preview URL", avatar_script['preview_url'])
                
            elif avatar_script and avatar_script.get('status') == 'failed':
                st.error(f"❌ Avatar creation failed: {avatar_script.get('error', 'Unknown error')}")
                
                # Show script preview even if avatar failed
                with st.expander("📝 Script Preview"):
                    script_preview = avatar_script.get('script_preview', 'No preview available')
                    st.text_area("Generated Script", value=script_preview, height=200, disabled=True)
                
                st.info("💡 The script was generated successfully, but the avatar creation failed. You can still use the script for manual presentation.")
                
            else:
                st.info("🎭 Avatar presentation will appear here when demo is generated")
                
                # Show sample avatar info
                st.markdown("""
                ### 🎭 Tavus Avatar Features
                
                Your avatar will:
                - 📖 Read the generated script naturally with AI voice
                - ⏸️ Pause at appropriate moments for emphasis
                - 👋 Use realistic gestures and expressions
                - 🎯 Adapt tone and pace for your audience
                - ⏱️ Follow the timing you specified
                - 🎨 Use professional presentation styling
                
                **To see the avatar in action:**
                1. Generate a demo above with your GitHub repo and requirements
                2. Wait for the Tavus API to create your avatar
                3. The avatar will appear here automatically
                """)

if __name__ == "__main__":
    main() 