import streamlit as st
from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline

st.set_page_config(page_title="AI Job Hunt Assistant", layout="centered")

st.title("AI Job Hunt Assistant")
st.markdown("Use AI agents to analyze jobs, tailor your resume, and write outreach messages — all from one interface.")

# input field
job_keyword = st.text_input("Job Keyword")
location = st.text_input("Location (ex: New York)")
resume_text = st.text_area("Resume text")
bio = st.text_input("Short user description")
   
if st.button("Search Jobs"):
    if not (job_keyword or location):
        st.warning("Missing required input")
    else:
        # 1. fetch jobs
        job_posts = fetch_usajobs(job_keyword, location, 5)

        if not job_posts:
            st.error("No job posting found")
        else:
            st.session_state["jobs"] = job_posts
            st.success("✅ Jobs Found!")


if "jobs" in st.session_state:

    selected_indexes = []

    """
    COUNTER-INTUITIVE DESIGN OF STREAMLIT:
    Every button click, text entry, or checkbox toggle triggers a complete re-run, 
    rebuilding selected_indexes from scratch with whatever boxes are currently checked!
    """

    """
    KEY CONCEPT: st.checkbox() is exactly the widget, "checkbox" is just variable that hold the value of true or false
    JUSTIFICATION:
    Streamlit re-runs the entire Python script from top to bottom on every user 
    interaction. When a widget includes a key parameter, Streamlit automatically 
    saves its state in st.session_state. On subsequent re-runs, the widget function 
    looks up that key in memory to return the saved user input, maintaining state 
    despite the script running from scratch. 
    """
    
    for i, job in enumerate(st.session_state["jobs"]): 
        job_data = job['MatchedObjectDescriptor']
        job_title = job_data.get("PositionTitle", "Unknown Title")
        job_agency = job_data.get('OrganizationName', 'Unknown Agency')
        
        # the variable is just used to hold "True" or "False"
        checkbox = st.checkbox(f"{job_title} — {job_agency}", key=f"job_{i}")

        if checkbox:
            # save the referecing index of that particular checkbox into the list
            selected_indexes.append(i)

    if st.button("Apply to Selected Jobs"):

        if not selected_indexes:
            st.warning("Please selected at least one job post")
        elif not resume_text.strip():
            st.warning("Please paste your resume before applying.")
        else:

            for index in selected_indexes:

                job_data = st.session_state["jobs"][i]['MatchedObjectDescriptor']

                # Wrap the slow code inside the spinner context
                with st.spinner(f"Applying to: {job_data.get('PositionTitle')}"):
                    # run the pipeline
                    result = run_pipeline(job, bio, resume_text)
                    st.markdown("---")
                    st.markdown(f"### The reach-out message for: {job_data.get('PositionTitle')}")
                    st.markdown(result)
                    