import streamlit as st
import requests

API_URL = "http://localhost:8000"

st.set_page_config(page_title="DSA Study Tracker", layout="wide")
st.title("DSA Tracker Dashboard")
st.write("Welcome to your local problem-solving database.")
st.divider()

def get_analytics():
    try:
        
        response = requests.get(f"{API_URL}/analytics/summary")
        response.raise_for_status()  
        return response.json()       
    except requests.exceptions.RequestException as e:
        st.error(f"Cannot connect to the backend API. Is your FastAPI server running? \nError: {e}")
        return None
    

summary_data = get_analytics()

if summary_data:
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Total Problems Logged", value=summary_data["total_problems"])
    
    with col2:
        st.metric(label="Successfully Solved", value=summary_data["total_solved"])
    
    with col3:
        st.metric(label="Total Time (Minutes)", value=summary_data["total_minutes"])


try:
    triage_resp = requests.get(f"{API_URL}/problems/triage")
    triage_list = triage_resp.json() if triage_resp.status_code == 200 else []
except:
    triage_list = []

if triage_list:
    st.divider()
    st.warning(f"🔔 **Inbox:** You have {len(triage_list)} synced problems missing study data!")
    
    current_problem = triage_list[0]
    
    with st.container(border=True): 
        st.subheader(f"⚡ Quick Log: {current_problem['title']}")
        st.caption(f"Topic: {current_problem['topic']} | Difficulty: {current_problem['difficulty']}")
        
        with st.form(f"triage_form_{current_problem['id']}", clear_on_submit=True):
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                duration = st.number_input("Estimated time spent (minutes)", min_value=1, step=5, value=20)
            with t_col2:
                status = st.selectbox("How did it go?", ["Confused", "Needed Hints", "Solved smoothly"])
            
            submit_triage = st.form_submit_button("Save & Next ➡️")
            
            if submit_triage:
                session_payload = {
                    "problem_id": current_problem['id'],
                    "duration_minutes": duration,
                    "status": status
                }
                # Log the session
                requests.post(f"{API_URL}/sessions/", json=session_payload)
                st.success("Saved!")
                st.rerun() 
st.divider()
st.subheader("AI Smart Coach")

try:
    coach_resp = requests.get(f"{API_URL}/analytics/coach")
    coach_data = coach_resp.json()
    
    if coach_data.get("status") == "success":
        topic = coach_data['weakest_topic']
        time = coach_data['avg_time']
        struggle = coach_data['struggle_rate']
        
        st.warning(f"**Focus Area:** You are struggling with **{topic}**.")

        st.write(f"You spend an average of **{time} minutes** per problem, and face friction **{struggle}%** of the time.")
        st.info(f" **Coach Recommendation:** Do not jump to Hard problems. Filter LeetCode for 'Easy' {topic} problems and master the base patterns first.")
    else:
        st.info(f"**Coach says:** {coach_data.get('message', 'Keep logging sessions!')}")
except Exception as e:
    st.error("Coach API is sleeping. Wake it up!")
st.divider()
st.header("Log Activity")


form_col1, form_col2 = st.columns(2)


with form_col1:
    st.subheader("Add New Problem")
    with st.form("add_problem_form", clear_on_submit=True):
        title = st.text_input("Problem Title (e.g., Two Sum)")
        difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
        topic = st.text_input("Topic (e.g., Arrays, Trees)")
        Solved = st.selectbox("Solved", [True,False])
        
        submit_problem = st.form_submit_button("Save Problem")
        
        if submit_problem and title and topic:
            payload = {
                "title": title, 
                "difficulty": difficulty, 
                "topic": topic, 
                "is_solved": Solved
            }
            # Send the POST request to your backend
            response = requests.post(f"{API_URL}/problems/", json=payload)
            if response.status_code == 200:
                st.success(f"Added '{title}' successfully!")
                st.rerun() 



with form_col2:
    st.subheader("Log Study Session")
    
    try:
        problems_req = requests.get(f"{API_URL}/problems/")
        problems_list = problems_req.json()
    except:
        problems_list = []
        
    with st.form("log_session_form", clear_on_submit=True):
        problem_options = {p["title"]: p["id"] for p in problems_list}
        
        selected_title = st.selectbox("Select Problem", options=list(problem_options.keys()))
        duration = st.number_input("Time Spent (minutes)", min_value=1, step=5, value=30)
        status = st.selectbox("How did it go?", ["Confused", "Needed Hints", "Solved smoothly"])
        
        
        st.write("") 
        mark_as_solved = st.checkbox("✅ Mark this problem as Solved!")
        
        submit_session = st.form_submit_button("Log Session")
        
        if submit_session and selected_title:
            problem_id = problem_options[selected_title]
            
            session_payload = {
                "problem_id": problem_id,
                "duration_minutes": duration,
                "status": status
            }
            response = requests.post(f"{API_URL}/sessions/", json=session_payload)
            
            if mark_as_solved:
                update_payload = {"is_solved": True}
                update_resp = requests.put(f"{API_URL}/problems/{problem_id}", json=update_payload)
                if update_resp.status_code != 200:
                    st.error(f"Backend rejected the update! Error: {update_resp.text}")
                    st.stop()
                
            if response.status_code == 200:
                st.success("Study session logged!")
                st.rerun()

st.divider()
st.header("Problem Library")

with st.expander("Auto-Sync with LeetCode"):
    col1, col2 = st.columns([3, 1])
    with col1:
        lc_username = st.text_input("Enter your LeetCode Username", placeholder="e.g., neetcode")
    with col2:
        st.write("") 
        st.write("")
        sync_btn = st.button("Sync Now")
        
    if sync_btn and lc_username:
        with st.spinner("Fetching data from LeetCode..."):
            sync_resp = requests.post(f"{API_URL}/sync/leetcode/{lc_username}")
            
            if sync_resp.status_code == 200:
                result = sync_resp.json()
                st.success(f"✅ {result['message']} Added: {result['added']}, Updated: {result['updated']}")
                import time
                time.sleep(2) 
                st.rerun()
            else:
                st.error("Failed to sync. Check the username and try again.")

if problems_list:
    st.dataframe(
        problems_list, 
        width="stretch", 
        hide_index=True,
        column_order=["id", "title", "difficulty", "topic", "url", "is_solved"],
        column_config={
            "url": st.column_config.LinkColumn("Problem Link", display_text="Open in LeetCode 🔗")
        }
    )
else:
    st.info("No problems logged yet. Add one above or Sync with LeetCode!")



