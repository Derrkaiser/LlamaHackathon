# TODO: Review and Customize System Prompt

## 📋 **Your Task: Review and Elaborate on the System Prompt**

The system prompt in `config.py` is the core instruction that guides Llama 4 Maverick in generating presentations. You should review and customize it based on your specific hackathon requirements.

## 🎯 **Current System Prompt Location**
File: `config.py`  
Variable: `SYSTEM_PROMPT`

## 🔍 **What to Review and Customize**

### 1. **Hackathon-Specific Requirements**
- [ ] **Target Audience**: Who are the judges/audience for your hackathon?
- [ ] **Evaluation Criteria**: What are the key criteria for winning?
- [ ] **Time Constraints**: How long do you have for the presentation?
- [ ] **Technical Focus**: What technical aspects should be emphasized?

### 2. **Presentation Style Preferences**
- [ ] **Tone**: Formal vs. casual, technical vs. business-focused
- [ ] **Structure**: Preferred presentation flow and sections
- [ ] **Visual Elements**: How should slides/demos be described?
- [ ] **Engagement**: How to keep the audience engaged?

### 3. **Demo Automation Requirements**
- [ ] **Browser Automation**: Specific tools or frameworks to mention
- [ ] **Avatar Integration**: How to coordinate with Tavus avatar
- [ ] **Timing**: Synchronization between demo and presentation
- [ ] **Fallback Scenarios**: What to do if automation fails?

### 4. **Technical Depth**
- [ ] **Code Explanation**: How detailed should technical explanations be?
- [ ] **Architecture Focus**: Which architectural aspects to highlight?
- [ ] **Innovation Emphasis**: What makes your solution unique?
- [ ] **Scalability**: How to present scalability and future potential?

## 📝 **Suggested Customizations**

### For Technical Hackathons:
```python
# Add to system prompt:
- Emphasize technical innovation and code quality
- Include code snippets and architecture diagrams
- Focus on performance, scalability, and best practices
- Highlight use of cutting-edge technologies
```

### For Business-Focused Hackathons:
```python
# Add to system prompt:
- Emphasize market opportunity and business model
- Include user stories and customer value
- Focus on revenue potential and competitive advantage
- Highlight team capabilities and execution plan
```

### For Innovation Hackathons:
```python
# Add to system prompt:
- Emphasize creativity and novel approaches
- Include problem-solution fit and market validation
- Focus on disruptive potential and industry impact
- Highlight unique technical or business insights
```

## 🎬 **Demo-Specific Instructions**

Consider adding specific instructions for:
- **Demo Flow**: How to structure the live demonstration
- **Error Handling**: What to do if things go wrong
- **Timing**: How to pace the presentation and demo
- **Q&A Preparation**: Anticipated questions and responses

## 🚀 **Next Steps**

1. **Review the current system prompt** in `config.py`
2. **Identify your hackathon's specific requirements**
3. **Customize the prompt** based on your needs
4. **Test the changes** using `test_integration.py`
5. **Iterate and refine** based on results

## 📊 **Testing Your Changes**

After customizing the system prompt:

```bash
# Test with a sample repository
python test_integration.py

# Test with the UI
streamlit run demo_ui.py
```

## 💡 **Tips for Effective Customization**

1. **Be Specific**: Include concrete examples and requirements
2. **Consider Audience**: Adapt language and depth to your judges
3. **Focus on Impact**: Emphasize what makes your solution compelling
4. **Include Constraints**: Mention time limits and technical requirements
5. **Prepare for Questions**: Anticipate what judges might ask

## 🔄 **Iteration Process**

1. Make changes to `SYSTEM_PROMPT` in `config.py`
2. Test with `test_integration.py`
3. Review generated presentations
4. Refine the prompt based on results
5. Repeat until satisfied

---
 