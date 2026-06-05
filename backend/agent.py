from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import os

load_dotenv()
print("API KEY:", os.getenv("GOOGLE_API_KEY"))

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

def generate_study_plan(hours):

    prompt = f"""
    Create a study plan for a student who can study {hours} hours daily.

    Include:
    - Morning Session
    - Afternoon Session
    - Evening Session
    - Break Times
    """

    response = llm.invoke(prompt)

    return response.content