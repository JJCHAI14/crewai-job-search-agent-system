from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.2,
    google_api_key=GEMINI_API_KEY
)

def get_jd_analyst_agent():

    analyst = Agent(
        role="Senior Job Description Analyst",
        goal="Understand and summarize government job postings",
        backstory="You're an expert in job market analysis with a focus on US federal job listings.",
        llm = llm_gemini,
        verbose=True
    )

    return analyst

def create_jd_analysis_task(analyst_agent, job_description):

    # construct Task instace 
    analysis_task = Task(
        description=f"""
        Analyze the following USAJobs job posting and extract:
        - A summary of the role
        - Key skills required
        - Any specific qualifications or eligibility
        \n\nJob Description:\n{job_description}
        """,
        expected_output="A structured markdown summary containing sections for Qualifications, Required Skills, and Responsibilities.",
        agent=analyst_agent,
        output_file='/data/report.md'
    )

    return analysis_task
    