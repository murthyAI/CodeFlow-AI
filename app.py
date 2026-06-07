import streamlit as st
import requests

# Configure OpenAI API Key (Replace with your active API key or set as environment variable)
API_KEY = "YOUR_OPENAI_API_KEY"
URL = "https://api.openai.com/v1/chat/completions"

# App Title and Description
st.set_page_config(page_title="CodeFlow AI - Code Tester & Reviewer", page_icon="🚀", layout="centered")
st.title("🚀 CodeFlow AI")
st.subheader("Automated Code Tester & Reviewer")
st.write("Paste your Python code below. The AI will automatically test it, find bugs, and optimize it for you!")

# User Code Input Box
user_code = st.text_area("Enter your Python code here:", height=250, placeholder="def my_function():\nprint('Hello World')")

# Analyze Button
if st.button("Analyze Code", type="primary"):
    if user_code.strip() != "":
        st.info("AI is analyzing your code... Please wait a moment...")
        
        # Headers and Payload for direct API Call
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        
        payload = {
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert Python code reviewer and tester. Provide a structured review in English with 3 clear sections: 1. Syntax Checker (issues found), 2. Auto-Bug Fixer (completely corrected code inside a markdown block), 3. Code Optimizer (efficiency and readability tips)."
                },
                {
                    "role": "user",
                    "content": f"Please analyze this code:\n```python\n{user_code}\n```"
                }
            ]
        }
        
        try:
            # Making the direct network call
            response = requests.post(URL, json=payload, headers=headers)
            response_data = response.json()
            
            if response.status_code == 200:
                st.success("Analysis Complete!")
                ai_analysis = response_data["choices"][0]["message"]["content"]
                st.markdown(ai_analysis)
            else:
                error_msg = response_data.get("error", {}).get("message", "Unknown error")
                st.error(f"API Error ({response.status_code}): {error_msg}")
                
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some code first before analyzing!")
