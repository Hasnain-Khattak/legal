import streamlit as st
import os
import hashlib
from src.document_processor import LegalDocumentProcessor
from src.vector_store import VectorStoreManager
from config.settings import settings

# Admin credentials (in production, use environment variables or secure storage)
ADMIN_CREDENTIALS = {
    "admin": "admin123",  # username: password
    # "manager": "manager456",
    # "superuser": "super789"
}

def hash_password(password):
    """Simple password hashing"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_password(username, password):
    """Verify user credentials"""
    if username in ADMIN_CREDENTIALS:
        return ADMIN_CREDENTIALS[username] == password
    return False

def login_page():
    """Display login page"""
    st.set_page_config(
        page_title="Admin Login - Document Management",
        page_icon="🔐",
        layout="centered"
    )
    
    # Login page styling
    st.markdown("""
    <style>
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem;
        border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        margin: 2rem 0;
    }
    .login-header {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    .login-form {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e2e8f0;
        padding: 0.75rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    .login-footer {
        text-align: center;
        margin-top: 2rem;
        color: #64748b;
        font-size: 0.9rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="login-container">
            <div class="login-header">
                <h1>🔐 Admin Portal</h1>
                <p>Document Management System</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # st.markdown('<div class="login-form">', unsafe_allow_html=True)
        
        st.markdown("### 🔑 Administrator Login")
        st.markdown("---")
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                login_button = st.form_submit_button("🚀 Login", use_container_width=True, type="primary")
            
            if login_button:
                if username and password:
                    if verify_password(username, password):
                        st.session_state.authenticated = True
                        st.session_state.username = username
                        st.success("✅ Login successful! Redirecting...")
                        st.rerun()
                    else:
                        st.error("❌ Invalid username or password!")
                else:
                    st.warning("⚠️ Please enter both username and password!")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # # Demo credentials info
        # with st.expander("🔍 Demo Credentials", expanded=False):
        #     st.markdown("**For testing purposes:**")
        #     st.code("Username: admin | Password: admin123")
        #     st.code("Username: manager | Password: manager456")
        #     st.code("Username: superuser | Password: super789")
        #     st.warning("⚠️ Change these credentials in production!")
        
        st.markdown("""
        <div class="login-footer">
            <p>🛡️ Secure Document Management System</p>
            <p>© 2024 Admin Dashboard. All rights reserved.</p>
        </div>
        """, unsafe_allow_html=True)

def logout():
    """Handle user logout"""
    st.session_state.authenticated = False
    st.session_state.username = None
    st.rerun()

def admin_dashboard():
    """Main admin dashboard (only accessible after login)"""
    st.set_page_config(
        page_title="Admin Dashboard - Document Management",
        page_icon="🔐",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for admin styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-align: center;
    }
    .admin-subtitle {
        color: #e5e7eb;
        text-align: center;
        margin-top: 0.5rem;
        font-size: 1.1rem;
    }
    .user-info {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-top: 1rem;
    }
    .admin-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
    .status-success {
        color: #059669;
        background-color: #ecfdf5;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #10b981;
        margin: 0.5rem 0;
    }
    .status-error {
        color: #dc2626;
        background-color: #fef2f2;
        padding: 0.5rem;
        border-radius: 5px;
        border-left: 4px solid #ef4444;
        margin: 0.5rem 0;
    }
    .sidebar .sidebar-content {
        background-color: #f8fafc;
    }
    .upload-section {
        border: 2px dashed #cbd5e1;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        background-color: #f8fafc;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header with user info
    st.markdown(f"""
    <div class="main-header">
        <h1>🔐 Admin Dashboard</h1>
        <div class="admin-subtitle">Document Management System</div>
        <div class="user-info">
            👤 Welcome, <strong>{st.session_state.username}</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize components
    if 'doc_processor' not in st.session_state:
        st.session_state.doc_processor = LegalDocumentProcessor(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
    
    if 'vector_store' not in st.session_state:
        st.session_state.vector_store = VectorStoreManager()
    
    # Sidebar for admin controls
    with st.sidebar:
        # User section
        st.markdown("### 👤 User Session")
        st.info(f"**Logged in as:** {st.session_state.username}")
        
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            logout()
        
        st.markdown("---")
        
        st.markdown("### 🛠️ Admin Controls")
        
        # System Status
        st.markdown("#### System Status")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Processor:** ✅")
        with col2:
            st.markdown("**Vector DB:** ✅")
        
        st.markdown("---")
        
        # Quick Actions
        st.markdown("#### Quick Actions")
        if st.button("🔄 Refresh Stats", use_container_width=True):
            st.rerun()
        
        if st.button("🗑️ Clear Session", use_container_width=True):
            # Keep authentication but clear other session data
            auth_state = st.session_state.authenticated
            username = st.session_state.username
            st.session_state.clear()
            st.session_state.authenticated = auth_state
            st.session_state.username = username
            st.rerun()
        
        st.markdown("---")
        
        # Settings
        st.markdown("#### Configuration")
        st.info(f"**Chunk Size:** {settings.CHUNK_SIZE}")
        st.info(f"**Chunk Overlap:** {settings.CHUNK_OVERLAP}")
    
    # Main dashboard content
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        st.markdown("### 📁 Document Upload Center")
        
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        st.markdown("**📤 Upload Legal Documents**")
        
        # File uploader
        uploaded_files = st.file_uploader(
            "Select PDF files to process",
            type=['pdf'],
            accept_multiple_files=True,
            help="Upload legal documents (PDFs) to add to the knowledge base",
            label_visibility="collapsed"
        )
        
        if uploaded_files:
            st.success(f"📋 {len(uploaded_files)} file(s) selected for processing")
            
            # Show selected files
            st.markdown("**Selected Files:**")
            for file in uploaded_files:
                st.markdown(f"• {file.name} ({file.size:,} bytes)")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("🚀 Process Documents", type="primary", disabled=not uploaded_files, use_container_width=True):
                if uploaded_files:
                    process_documents(uploaded_files)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        st.markdown("### 📊 System Statistics")
        
        # Statistics cards
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="📄 Documents Processed", 
            value=st.session_state.get('docs_processed', 0),
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="🧩 Total Chunks", 
            value=st.session_state.get('total_chunks', 0),
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric(
            label="💾 Storage Status", 
            value="Active",
            delta=None
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Activity Log
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        st.markdown("### 📝 Activity Log")
        
        if 'processing_status' in st.session_state:
            for status in st.session_state.processing_status[-5:]:  # Show last 5 entries
                if "✅" in status:
                    st.markdown(f'<div class="status-success">{status}</div>', unsafe_allow_html=True)
                elif "❌" in status:
                    st.markdown(f'<div class="status-error">{status}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"• {status}")
        else:
            st.markdown("*No recent activity*")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Processing status section
    if 'processing_status' in st.session_state and len(st.session_state.processing_status) > 5:
        st.markdown("---")
        st.markdown('<div class="admin-card">', unsafe_allow_html=True)
        st.markdown("### 📋 Complete Processing Log")
        
        with st.expander("View All Processing Events", expanded=False):
            for status in st.session_state.processing_status:
                if "✅" in status:
                    st.markdown(f'<div class="status-success">{status}</div>', unsafe_allow_html=True)
                elif "❌" in status:
                    st.markdown(f'<div class="status-error">{status}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f"• {status}")
        
        st.markdown('</div>', unsafe_allow_html=True)

def process_documents(uploaded_files):
    """Process uploaded documents"""
    st.session_state.processing_status = []
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    all_documents = []
    
    for i, uploaded_file in enumerate(uploaded_files):
        progress = (i + 1) / len(uploaded_files)
        progress_bar.progress(progress)
        status_text.text(f"🔄 Processing {uploaded_file.name}... ({i+1}/{len(uploaded_files)})")
        
        try:
            # Process document
            documents = st.session_state.doc_processor.process_uploaded_file(uploaded_file)
            all_documents.extend(documents)
            
            st.session_state.processing_status.append(
                f"✅ {uploaded_file.name}: {len(documents)} chunks processed"
            )
            
        except Exception as e:
            st.session_state.processing_status.append(
                f"❌ {uploaded_file.name}: Error - {str(e)}"
            )
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
    
    # Store all documents in vector store
    if all_documents:
        status_text.text("💾 Storing documents in vector database...")
        if st.session_state.vector_store.store_documents(all_documents):
            st.success(f"🎉 Successfully processed and stored {len(all_documents)} document chunks!")
            
            # Update statistics
            st.session_state.docs_processed = st.session_state.get('docs_processed', 0) + len(uploaded_files)
            st.session_state.total_chunks = st.session_state.get('total_chunks', 0) + len(all_documents)
            
        else:
            st.error("❌ Failed to store documents in vector database!")

    progress_bar.progress(1.0)
    status_text.text("✅ Processing complete!")

def main():
    """Main application entry point"""
    # Check authentication status
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Route to appropriate page
    if st.session_state.authenticated:
        admin_dashboard()
    else:
        login_page()

if __name__ == "__main__":
    main()