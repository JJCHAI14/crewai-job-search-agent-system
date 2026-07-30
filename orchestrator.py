import re
from crewai import Crew, Process
from usajobs_api import fetch_usajobs
from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from utils.tracking import save_cover_letter_file, log_application

def load_resume(filename):
    with open(filename,'r') as f:
        return f.read()

def extract_between_markers(resume_output):
    pattern = r'(?=<<COVER_LETTER>>)'
    output = re.split(pattern, resume_output)
    return output

def run_pipeline(job_data, user_bio, resume_text):

    # 1. Extract job description from the first result
    job_summary = job_data['UserArea']['Details']['JobSummary']
    job_agency = job_data.get('OrganizationName', 'Unknown Agency')
    job_title = job_data.get('PositionTitle', 'Unknown Position')

    # 3. Initialize JD agent and task
    jd_agent = get_jd_analyst_agent()
    jd_task = create_jd_analysis_task(jd_agent, job_summary)

    # 4. Initialize resume writing agent and task
    resume_writing_agent = get_resume_cl_agent()
    resume_writing_task = create_resume_cl_task(resume_writing_agent, job_summary, resume_text)

    # 5. Initialize message writing agent and task
    messaging_agent = get_messaging_agent()
    messaging_task = create_messaging_task(messaging_agent, job_summary, job_agency, user_bio)

    # 5. initialize crew
    # create a crew to take the analyst and task
    my_crew = Crew(
        agents=[jd_agent, resume_writing_agent, messaging_agent],
        tasks=[jd_task, resume_writing_task, messaging_task],
        process=Process.sequential
    )

    # kick off the crew
    result = my_crew.kickoff()

    resume_output = str(resume_task.output)
    splitted_resume = extract_between_markers(resume_output)
    
    # Log and save
    log_application(job_title, job_agency, splitted_resume[0])
    save_cover_letter_file(job_title, splitted_resume[1])

    return result

if __name__ == "__main__":
    # 2. load resume
    """
    resume_text = load_resume("./data/sample_resume.txt")

    job_posts = fetch_usajobs("Data Analyst", "New York")
    first_job = job_posts[0]
    user_bio1="Professional data analyst with 5 years experience in fintech company"

    run_pipeline(first_job, user_bio1, resume_text)
    """

    resume_summary = """
    <<RESUME_SUMMARY>> 
    This is the summary 
    
    <<COVER_LETTER>>
    This is the cover leter
    """

    output = extract_between_markers(resume_summary)
    print(output[0])
    print("====")
    print(output[1])
    
