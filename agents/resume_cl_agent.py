from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.3, # 0.3 for slightly more creative output
    google_api_key=GEMINI_API_KEY
)

def get_resume_cl_agent():

    writer_agent = Agent(
        role="Resume & Cover Letter Writer",
        goal="Customize application materials to match job descriptions",
        backstory="You're an expert in professional writing and tailoring resumes for job applications, especially in government and tech roles.",
        llm=llm_gemini,
        verbose=True
    )

    return writer_agent

def create_resume_cl_task(agent, job_summary, resume_text):

    writing_task = Task(
        description=f"""
        Based on the job summary below, tailor the candidate's resume summary and generate a personalized cover letter.
        
        --- Job Summary ---
        {job_summary}
        
        --- Resume Text ---
        {resume_text}
        
        Your output should include:
        1. Updated professional summary for resume
        2. A personalized cover letter suitable for a government job
        """,
        expected_output=""" 
        <<RESUME_SUMMARY>>
        [Your tailored 3-5 sentence resume summary here]

        <<COVER_LETTER>>
        [Your personalized cover letter here]
        """,
        agent=agent,
        output_file="/data/resume_agent_output.txt"
    )

    return writing_task