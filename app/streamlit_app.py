import sys
import os
from datetime import datetime

# Fix import path issue
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from streamlit_chat import message

from src.pipeline.rag_pipeline import build_index, run_pipeline

# Page config
st.set_page_config(
    page_title="DocuMind AI Chatbot", 
    page_icon="📚", 
    layout="wide"
)

# Custom CSS for better UI
st.markdown("""
<style>
    .stTextInput > div > div > input {
        font-size: 16px;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .user-message {
        background-color: #e3f2fd;
        align-items: flex-end;
    }
    .bot-message {
        background-color: #f5f5f5;
        align-items: flex-start;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# INITIALIZE SESSION STATE
# =========================
if "index_built" not in st.session_state:
    st.session_state.index_built = False
    
if "messages" not in st.session_state:
    st.session_state.messages = []
    
if "uploaded_files_list" not in st.session_state:
    st.session_state.uploaded_files_list = []
    
if "documents_processed" not in st.session_state:
    st.session_state.documents_processed = False

# =========================
# SIDEBAR - DOCUMENT MANAGEMENT
# =========================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/google-docs.png", width=80)
    st.title("📄 Document Management")
    
    # File upload section
    st.markdown("### 📤 Upload Documents")
    uploaded_files = st.file_uploader(
        "Choose PDF, DOCX, or TXT files",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True,
        key="file_uploader"
    )
    
    if uploaded_files:
        save_path = "data/raw"
        os.makedirs(save_path, exist_ok=True)
        
        for file in uploaded_files:
            if file.name not in st.session_state.uploaded_files_list:
                file_path = os.path.join(save_path, file.name)
                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())
                st.session_state.uploaded_files_list.append(file.name)
        
        st.success(f"✅ {len(uploaded_files)} file(s) uploaded!")
        st.session_state.documents_processed = False
    
    # Show uploaded files
    if st.session_state.uploaded_files_list:
        st.markdown("### 📁 Your Documents")
        for doc in st.session_state.uploaded_files_list:
            st.write(f"📄 {doc}")
    
    # Build index button
    st.markdown("---")
    st.markdown("### ⚙️ Index Management")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔨 Build Index", use_container_width=True):
            with st.spinner("Processing documents..."):
                try:
                    data = build_index()
                    st.session_state.index_built = True
                    st.session_state.documents_processed = True
                    
                    # Add system message
                    st.session_state.messages.append({
                        "role": "system",
                        "content": f"✅ Indexed {data['num_documents']} documents into {data['num_chunks']} chunks. You can now ask questions!",
                        "timestamp": datetime.now()
                    })
                    st.success(f"Indexed {data['num_documents']} docs into {data['num_chunks']} chunks")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error building index: {str(e)}")
    
    with col2:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
    
    # Status indicator
    st.markdown("---")
    if st.session_state.index_built:
        st.success("✅ Index is ready!")
    else:
        st.warning("⚠️ Please build index first")

# =========================
# MAIN CHAT INTERFACE
# =========================
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🤖 DocuMind AI Chatbot")
    st.caption("Your Enterprise RAG-Powered Document Intelligence Assistant")

# Welcome message
if not st.session_state.messages:
    st.session_state.messages.append({
        "role": "assistant",
        "content": "👋 Hello! I'm DocuMind AI, your document intelligence assistant.\n\n"
                   "**Here's how to use me:**\n"
                   "1. 📤 Upload documents using the sidebar\n"
                   "2. 🔨 Click 'Build Index' to process them\n"
                   "3. 💬 Start asking questions about your documents!\n\n"
                   "What would you like to know?",
        "timestamp": datetime.now()
    })

# =========================
# DISPLAY CHAT HISTORY
# =========================
chat_container = st.container()

with chat_container:
    for msg in st.session_state.messages:
        if msg["role"] != "system":  # Don't show system messages in chat
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                st.caption(f"🕒 {msg['timestamp'].strftime('%H:%M:%S')}")

# =========================
# CHAT INPUT
# =========================
st.markdown("---")

# Check if index is built before allowing questions
if not st.session_state.index_built:
    st.info("📚 **Ready to get started?** Upload documents in the sidebar and click 'Build Index' to begin!")
    query = st.chat_input("👆 Please build the index first to start asking questions", disabled=True)
else:
    query = st.chat_input("💬 Ask me anything about your documents...")

# =========================
# PROCESS QUERY
# =========================
if query and st.session_state.index_built:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": query,
        "timestamp": datetime.now()
    })
    
    # Display user message immediately
    with st.chat_message("user"):
        st.markdown(query)
        st.caption(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🤔 Thinking..."):
            try:
                result = run_pipeline(query)
                
                # Display answer
                st.markdown(result["answer"])
                
                # Display confidence with progress bar
                confidence = result.get("confidence", 70)
                st.progress(confidence / 100)
                st.caption(f"📊 Confidence: {confidence}%")
                
                # Display sources in expander
                if result.get("sources"):
                    with st.expander("📚 View Sources"):
                        for i, src in enumerate(result["sources"], 1):
                            st.markdown(f"**{i}. {src.get('source', 'Unknown')}** (Page {src.get('page', 'N/A')})")
                            if src.get('text'):
                                st.text(f"Excerpt: {src['text'][:200]}...")
                
                st.caption(f"🕒 {datetime.now().strftime('%H:%M:%S')}")
                
                # Add to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "timestamp": datetime.now(),
                    "sources": result.get("sources", []),
                    "confidence": confidence
                })
                
            except Exception as e:
                error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_msg,
                    "timestamp": datetime.now()
                })

# =========================
# FOOTER WITH STATS
# =========================
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("📄 Documents", len(st.session_state.uploaded_files_list))
with col2:
    st.metric("💬 Messages", len([m for m in st.session_state.messages if m["role"] != "system"]))
with col3:
    status = "✅ Ready" if st.session_state.index_built else "⚠️ Not Indexed"
    st.metric("⚙️ Status", status)