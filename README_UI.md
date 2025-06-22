# 🚀 Llama Hackathon Demo Generator UI

A beautiful Streamlit interface for generating AI-powered presentations using Llama 4 Maverick.

## Features

- 📄 **PDF Requirements Upload**: Upload or provide path to requirements documents
- 🔗 **GitHub Repo Integration**: Connect your GitHub repository for codebase analysis
- 🎭 **Audience Customization**: Tailor presentations for different audience types
- ⏱️ **Duration Control**: Set presentation length (3-15 minutes)
- 🎯 **Focus Areas**: Select what features to emphasize
- 🤖 **Llama 4 Maverick**: Powered by advanced AI analysis
- 📊 **Real-time Analysis**: Get insights and recommendations

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_ui.txt
```

### 2. Set Environment Variables

Create a `.env` file in the project root:

```bash
LLAMA_API_KEY=your_llama_api_key_here
TAVUS_API_KEY=your_tavus_api_key_here  # Optional for avatar features
```

### 3. Run the UI

```bash
streamlit run demo_ui.py
```

The UI will open in your browser at `http://localhost:8501`

## Usage

### Step 1: Project Information
- **GitHub Repository URL**: Enter your repo URL for codebase analysis
- **Requirements Document**: Upload a PDF or provide file path
- **Demo Duration**: Select presentation length

### Step 2: Presentation Details
- **Target Audience**: Choose audience type (Technical, Business, etc.)
- **Demo Purpose**: Select presentation goal
- **Focus Areas**: Choose what to emphasize

### Step 3: Advanced Configuration
- **Llama API Key**: Your Llama API credentials
- **Demo URL**: Optional - we'll try to discover it automatically
- **Analysis Options**: Toggle detailed analysis features

### Step 4: Generate
Click "Generate AI Presentation" to:
- Analyze requirements and codebase
- Generate presentation script
- Create demo execution plan
- Provide analysis summary

## Output

The system generates three main outputs:

### 📝 Presentation Script
- Structured content for Tavus avatar
- Timing markers and gesture cues
- Demo triggers for synchronization

### 🎬 Demo Plan
- Step-by-step execution instructions
- Browser automation commands
- Visual asset requirements

### 📊 Analysis Summary
- Project insights and metrics
- Technical complexity assessment
- Risk factors and recommendations

## Integration Points

### For Your Partner's GitHub Analysis
Update the `_process_codebase()` method in `ui_integration.py` to integrate with your partner's GitHub repo analysis code.

### For Tavus Avatar Integration
The presentation script is formatted for Tavus avatar integration with timing markers and gesture cues.

### For Demo Orchestration
The agent execution plan provides structured commands for browser automation and visual generation.

## Customization

### Adding New Audience Types
Edit the `audience_type` options in `demo_ui.py`

### Adding New Focus Areas
Update the `focus_areas` options in `demo_ui.py`

### Modifying Analysis Prompts
Edit the prompt templates in `ui_integration.py`

## Troubleshooting

### API Key Issues
- Ensure your Llama API key is valid
- Check API usage limits and credits
- Verify the API key format

### PDF Parsing Issues
- Ensure PDF is not password protected
- Check file format compatibility
- Try providing file path instead of upload

### Integration Issues
- Check all dependencies are installed
- Verify import paths are correct
- Review error logs for specific issues

## Development

### File Structure
```
├── demo_ui.py              # Main Streamlit UI
├── ui_integration.py       # Backend integration logic
├── requirements_ui.txt     # UI dependencies
├── src/                    # Core functionality
│   ├── analysis/          # PDF parsing
│   └── core/              # Llama client
└── README_UI.md           # This file
```

### Adding New Features
1. Update UI components in `demo_ui.py`
2. Add processing logic in `ui_integration.py`
3. Update integration tests
4. Document new features

## Hackathon Demo Tips

### For Judges
- Show the UI interface first
- Demonstrate PDF upload and analysis
- Show generated presentation script
- Highlight the AI-powered insights

### For Live Demo
- Have a sample PDF ready
- Prepare a GitHub repo URL
- Test with your Llama API key
- Have backup demo data ready

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review error messages carefully
3. Verify all dependencies are installed
4. Test with sample data first

---

Built with ❤️ for the Llama Hackathon | Powered by Llama 4 Maverick & Tavus 