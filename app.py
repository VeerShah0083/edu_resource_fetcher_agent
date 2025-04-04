import streamlit as st
from academic_agent import AcademicResourceGatherer
import time
from typing import Dict
import json
import random

# Set page config
st.set_page_config(
    page_title="EduHub - Your Learning Companion",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        margin: 10px 0;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .resource-card {
        background-color: white;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        transition: transform 0.3s ease;
    }
    .resource-card:hover {
        transform: translateY(-5px);
    }
    .category-title {
        color: #2c3e50;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
    }
    .resource-link {
        color: #2196F3;
        text-decoration: none;
        transition: color 0.3s ease;
        display: block;
        padding: 8px 0;
        font-size: 16px;
    }
    .resource-link:hover {
        color: #1976D2;
    }
    .feature-card {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    .stats-container {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        flex-wrap: wrap;
    }
    .stat-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 10px;
        flex: 1;
        min-width: 200px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 8px;
        padding: 12px;
        background-color: white;
        color: #2c3e50;
    }
    .stTextInput>div>div>input:focus {
        border-color: #4CAF50;
    }
    .stMarkdown {
        color: #2c3e50;
    }
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
        color: #2c3e50;
    }
    .stMarkdown p {
        color: #2c3e50;
    }
    .stMarkdown li {
        color: #2c3e50;
    }
    .stTextInput>label {
        color: black !important;
    }
    .stSpinner>div>div>div {
        color: black !important;
    }
    </style>
""", unsafe_allow_html=True)

def display_resources(resources: Dict):
    """Display resources in a beautiful card format"""
    for category, items in resources.items():
        if items:  # Only show categories that have items
            st.markdown(f"""
                <div class="resource-card">
                    <h2 class="category-title">📌 {category}</h2>
            """, unsafe_allow_html=True)
            
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        title = item.get('title', '')
                        url = item.get('url', '')
                        if title and url:
                            st.markdown(f"""
                                <a href="{url}" target="_blank" class="resource-link">
                                    • {title}
                                </a>
                            """, unsafe_allow_html=True)
            else:
                st.markdown(f"• {items}")
            
            st.markdown("</div>", unsafe_allow_html=True)

def main():
    # Initialize session state for topic
    if 'current_topic' not in st.session_state:
        st.session_state.current_topic = None
    
    # Header with gradient background
    st.markdown("""
        <div style='background: linear-gradient(135deg, #4CAF50, #45a049); padding: 40px; border-radius: 15px; margin-bottom: 30px;'>
            <h1 style='color: white; text-align: center; margin: 0; font-size: 2.5em;'>🎓 EduHub</h1>
            <p style='color: white; text-align: center; margin: 10px 0 0; font-size: 1.2em;'>Your AI-Powered Learning Companion</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Stats section
    st.markdown("""
        <div class="stats-container">
            <div class="stat-card">
                <h3>📚</h3>
                <p>Learning Resources</p>
            </div>
            <div class="stat-card">
                <h3>🎯</h3>
                <p>Topics Covered</p>
            </div>
            <div class="stat-card">
                <h3>👥</h3>
                <p>Active Learners</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #4CAF50, #45a049); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
                <h2 style='color: white; margin: 0;'>About EduHub</h2>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <h3>🎯 Smart Learning</h3>
                <p>AI-powered resource recommendations</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <h3>📚 Comprehensive Resources</h3>
                <p>Curated learning materials</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="feature-card">
                <h3>📱 Mobile Friendly</h3>
                <p>Learn anywhere, anytime</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.header("How to Use")
        st.markdown("""
            1. 🔍 Enter your topic
            2. 📚 Browse resources
            3. 🎯 Start learning
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        topic = st.text_input("What would you like to learn about?", 
                            value=st.session_state.current_topic if st.session_state.current_topic else "",
                            placeholder="e.g., Machine Learning, Quantum Physics, etc.",
                            label_visibility="visible")
        
        if st.button("Find Learning Resources", key="search_button"):
            if topic:
                # Update session state
                st.session_state.current_topic = topic
                
                with st.spinner("🔍 Searching for the best learning resources..."):
                    # Initialize the gatherer
                    gatherer = AcademicResourceGatherer()
                    
                    # Add a progress bar
                    progress_bar = st.progress(0)
                    
                    # Simulate progress
                    for i in range(100):
                        time.sleep(0.01)
                        progress_bar.progress(i + 1)
                    
                    # Get resources
                    resources = gatherer.gather_resources(topic)
                    
                    # Clear progress bar
                    progress_bar.empty()
                    
                    # Display results
                    st.markdown(f"""
                        <h2 style='text-align: center; color: #2c3e50; margin: 20px 0;'>
                            📚 Learning Resources for "{topic}"
                        </h2>
                    """, unsafe_allow_html=True)
                    
                    display_resources(resources)
            else:
                st.warning("Please enter a topic to search for resources.")
    
    with col2:
        st.markdown("""
            <div style='background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3 style='color: #2c3e50;'>🎯 Popular Topics</h3>
                <ul style='list-style: none; padding: 0;'>
                    <li style='margin: 10px 0;'>• Machine Learning</li>
                    <li style='margin: 10px 0;'>• Web Development</li>
                    <li style='margin: 10px 0;'>• Data Science</li>
                    <li style='margin: 10px 0;'>• Artificial Intelligence</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div style='background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-top: 20px;'>
                <h3 style='color: #2c3e50;'>💡 Learning Tips</h3>
                <ul style='list-style: none; padding: 0;'>
                    <li style='margin: 10px 0;'>• Start with basics</li>
                    <li style='margin: 10px 0;'>• Practice regularly</li>
                    <li style='margin: 10px 0;'>• Join communities</li>
                    <li style='margin: 10px 0;'>• Build projects</li>
                </ul>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 