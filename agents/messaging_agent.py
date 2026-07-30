from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

llm_gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    temperature=0.2,
    google_api_key=GEMINI_API_KEY
)

def get_messaging_agent():
    messaging_agent = Agent(
        role="Outreach Message Writer",
        goal="Draft personalized messages for job outreach",
        backstory="You're a professional career coach skilled in writing effective cold emails and outreach messages for job seekers in tech and government.",
        llm = llm_gemini,
        verbose=True
    )

    return messaging_agent

def create_messaging_task(agent, job_summary, agency_name, user_bio):

    messaging_task = Task(
        description=f"""
        Write a concise and compelling outreach message that the candidate could send to someone at {agency_name}, expressing interest in the job described below.
        
        --- Job Summary ---
        {job_summary}
        
        --- Candidate Bio ---
        {user_bio}
        
        The message should be friendly, professional, and under 150 words. Tailor it for a platform like LinkedIn or email.
        """,
        expected_output="A short outreach message under 150 words, tailored for LinkedIn or email, that is professional and expresses interest in the job at the given agency.",
        agent=agent
        
    )

    return messaging_task


if __name__ == "__main__":

    # Get and print the current working directory
    current_path = Path.cwd()
    print(f"Current Working Directory: {current_path}")