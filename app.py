import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Set up page configuration
st.set_page_config(page_title="App Monitor", layout="wide")

# Auto-refresh every 5 minutes (300,000 ms)
refresh_count = st_autorefresh(interval=300000, limit=None, key="refresher")

# Initialize session state for tracking history
if 'history' not in st.session_state:
    st.session_state.history = []

# Apps to monitor
apps = [
    {"name": "dorkerator", "url": "https://dorkerator.streamlit.app/"},
    {"name": "cipherbox", "url": " https://cipherbox.streamlit.app/"},
    {"name": "qrgen", "url": "https://qrgen-app.streamlit.app/"},
    {"name": "exifexplorer", "url": "https://exifexplorer.streamlit.app/"},
    {"name": "passcheq", "url": "https://passcheq.streamlit.app/"},
    {"name": "xmlsgv", "url": "https://xmlsgv.streamlit.app/"},
    {"name": "App Monitor", "url": "https://appmon.streamlit.app"}
   
]

st.title("Streamlit App Monitor")
st.write(f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Refresh #{refresh_count})")

# Function to check app status
def check_app_status(app_url):
    try:
        start_time = time.time()
        response = requests.get(app_url, timeout=15)
        response_time = (time.time() - start_time) * 1000  # in ms
        
        return {
            "status": "Online" if response.status_code == 200 else f"Error: {response.status_code}",
            "response_time": f"{response_time:.2f} ms",
            "timestamp": datetime.now()
        }
    except Exception as e:
        return {
            "status": f"Error: {str(e)}",
            "response_time": "N/A",
            "timestamp": datetime.now()
        }

# Create status dashboard
st.subheader("Current Status")

# Create columns for each app
cols = st.columns(len(apps))

# Check status for each app and display
current_statuses = []
for i, app in enumerate(apps):
    status_info = check_app_status(app["url"])
    current_statuses.append({
        "app_name": app["name"],
        "url": app["url"],
        **status_info
    })
    
    with cols[i]:
        st.write(f"### {app['name']}")
        st.write(f"URL: {app['url']}")
        
        if "Online" in status_info["status"]:
            st.success(f"Status: {status_info['status']}")
        else:
            st.error(f"Status: {status_info['status']}")
            
        st.write(f"Response Time: {status_info['response_time']}")

# Add current statuses to history
st.session_state.history.extend(current_statuses)

# Keep only the last 100 entries in history
if len(st.session_state.history) > 100:
    st.session_state.history = st.session_state.history[-100:]

# Display history
st.subheader("Monitoring History")
history_df = pd.DataFrame(st.session_state.history)
if not history_df.empty:
    history_df["timestamp"] = pd.to_datetime(history_df["timestamp"])
    history_df = history_df.sort_values("timestamp", ascending=False)
    st.dataframe(history_df)
else:
    st.write("No history available yet.")
