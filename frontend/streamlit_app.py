import streamlit as st
import websocket
import requests

# Set page to wide mode to give the feed more room
st.set_page_config(page_title="Anonymous Support & Social Feed", page_icon="💬", layout="wide")
if "post_limit" not in st.session_state:
    st.session_state.post_limit = 10
# ================================
# SIDEBAR: AI THERAPIST CHAT
# ================================
with st.sidebar:
    st.title("💬 Anonymous Chat")
    st.caption("A safe, private space to talk with the AI therapist.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "ws" not in st.session_state:
        try:
            ws = websocket.create_connection("ws://127.0.0.1:8000/api/ws/chat")
            system_welcome = ws.recv()
            st.session_state.ws = ws
        except Exception as e:
            st.error("Could not connect to Chat. Is the FastAPI server running?")

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input (This will automatically pin to the bottom of the sidebar)
    if prompt := st.chat_input("What is on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Listening..."):
                try:
                    st.session_state.ws.send(prompt)
                    response = st.session_state.ws.recv()
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                
                # --- NEW AUTO-RECONNECT LOGIC ---
                except Exception as e:
                    st.warning("Connection refreshed. Please try sending your message again.")
                    
                    # Delete the broken socket from memory
                    if "ws" in st.session_state:
                        del st.session_state.ws
                        
                    # Rerun the app to trigger a fresh connection at the top of the script
                    st.rerun()

# ================================
# MAIN PAGE: SOCIAL FEED
# ================================
# --- ADMIN DASHBOARD TOGGLE ---
# --- ADMIN DASHBOARD TOGGLE & AUTH ---
st.sidebar.divider()
admin_password = st.sidebar.text_input("🔒 Admin Access", type="password", placeholder="Enter password")

# Use a hardcoded password for development (e.g., "supersecret")
if admin_password == "supersecret":
    st.title("📊 Platform Analytics")
    st.write("Monitor engagement and user activation metrics.")
    
    try:
        stats_res = requests.get(f"{API_BASE_URL}/stats")
        if stats_res.status_code == 200:
            stats = stats_res.json()
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Posts", stats["total_posts"])
            col2.metric("Text Only", stats["text_only"])
            col3.metric("Images", stats["images"])
            col4.metric("Videos", stats["videos"])
            
            st.divider()
            
            st.bar_chart({
                "Text": stats["text_only"], 
                "Images": stats["images"], 
                "Videos": stats["videos"]
            })
            
    except Exception as e:
        st.error("Could not load analytics.")
        
    st.stop() # Hides the public feed
    
elif admin_password:
    # If they typed something but it's wrong
    st.sidebar.error("Access denied.")
st.title("Community Feed")
st.write("Share your thoughts, images, or videos completely anonymously.")

API_BASE_URL = "http://127.0.0.1:8000/api/posts"

# 1. Create a Post Form
with st.container():
    st.subheader("Create a Post")
    with st.form("post_form", clear_on_submit=True):
        post_content = st.text_area("Write something to the community...")
        post_file = st.file_uploader("Upload an Image or Video", type=["png", "jpg", "jpeg", "mp4", "mov"])
        
        submitted = st.form_submit_button("Post Anonymously")
        if submitted:
            if not post_content and not post_file:
                st.warning("Please write something or upload a file.")
            else:
                files = {}
                data = {"content": post_content}
                
                # If a file was selected, package it for the FastAPI endpoint
                if post_file:
                    files = {"file": (post_file.name, post_file.getvalue(), post_file.type)}
                
                # Send the HTTP POST request to your backend
                res = requests.post(f"{API_BASE_URL}/", data=data, files=files)
                if res.status_code == 200:
                    st.success("Posted successfully!")
                    st.rerun() # Refresh the page to show the new post
                else:
                    st.error("Failed to post.")

st.divider()

# 2. Display the Feed
st.subheader("Recent Posts")
try:
    # Pass the limit parameter to the FastAPI backend
    params = {"limit": st.session_state.post_limit, "offset": 0}
    response = requests.get(f"{API_BASE_URL}/", params=params)
    
    if response.status_code == 200:
        posts = response.json()
        if not posts:
            st.info("No posts yet. Be the first to share!")
        
        for post in posts:
            with st.container(border=True):
                date_str = post["created_at"].split("T")[0]
                st.caption(f"Anonymous User • {date_str}")
                
                if post["content"]:
                    st.markdown(post["content"])
                
                if post["media_url"]:
                    media_url = f"http://127.0.0.1:8000{post['media_url']}"
                    if post["media_type"] == "image":
                        st.image(media_url)
                    elif post["media_type"] == "video":
                        st.video(media_url)
        
        # --- THE PAGINATION BUTTON ---
        # If the number of posts returned equals our limit, there might be more in the database
        if len(posts) == st.session_state.post_limit:
            if st.button("Load More Posts"):
                st.session_state.post_limit += 10
                st.rerun()
                
    else:
        st.error("Could not fetch the feed.")
except Exception as e:
    st.error("Ensure your backend server is running to see the feed.")