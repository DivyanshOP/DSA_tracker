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
        response.raise_for_status()  # This will raise an error if the backend crashes
        return response.json()       # Converts the JSON into a Python dictionary
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



st.divider()
st.header("📝 Log Activity")

# Create two columns for our two forms
form_col1, form_col2 = st.columns(2)

# --- FORM 1: ADD A NEW PROBLEM ---
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
                st.rerun() # Instantly refreshes the page to update your dashboard numbers

# --- FORM 2: LOG A STUDY SESSION ---
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
        
        # NEW: A simple checkbox right before the submit button
        st.write("") # Little visual spacer
        mark_as_solved = st.checkbox("✅ Mark this problem as Solved!")
        
        submit_session = st.form_submit_button("Log Session")
        
        if submit_session and selected_title:
            problem_id = problem_options[selected_title]
            
            # 1. Log the study session (POST)
            session_payload = {
                "problem_id": problem_id,
                "duration_minutes": duration,
                "status": status
            }
            response = requests.post(f"{API_URL}/sessions/", json=session_payload)
            
            # 2. Update the problem status IF they checked the box (PUT)
            if mark_as_solved:
                update_payload = {"is_solved": True}
                update_resp = requests.put(f"{API_URL}/problems/{problem_id}", json=update_payload)
                if update_resp.status_code != 200:
                    st.error(f"Backend rejected the update! Error: {update_resp.text}")
                    st.stop()
                
            if response.status_code == 200:
                st.success("Study session logged!")
                st.rerun()
# --- SECTION 3: PROBLEM LIBRARY & UPDATES ---
st.divider()
st.header("Problem Library")

# 1. Display the database as a clean interactive table
if problems_list:
    # Streamlit automatically turns a list of dictionaries into a beautiful table
    st.dataframe(
        problems_list, 
        # use_container_width=True,
        width="stretch", 
        hide_index=True,
        column_order=["id", "title", "difficulty", "topic", "is_solved"] # Forces a clean column order
    )
else:
    st.info("No problems logged yet. Add one above!")


