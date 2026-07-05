import streamlit as st
import time
from components.icons import get_icon

def animated_loading(task_func, *args, **kwargs):
    """
    Shows an animated progress using st.status and executes task_func
    without emojis, using professional copy.
    """
    with st.status("Initializing Analysis...", expanded=True) as status:
        st.write("Extracting resume structure...")
        time.sleep(0.5)
        st.write("Analyzing job requirements...")
        time.sleep(0.5)
        st.write("Evaluating compatibility with Gemini AI...")
        
        # Execute the actual function
        result = task_func(*args, **kwargs)
        
        st.write("Compiling final recommendations...")
        time.sleep(0.5)
        status.update(label="Analysis Complete", state="complete", expanded=False)
        
    return result
