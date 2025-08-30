from agents import Agent, RunContextWrapper, Runner, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich

from dotenv import load_dotenv
load_dotenv()

# 👤 User Context
class Person(BaseModel):
    name: str
    user_type: str   # Patient | Medical Student | Doctor

# Example user
personOne = Person(
    name="Saba",
    user_type="Patient"  # Change this to "Medical Student" or "Doctor"
)

# 🧠 Dynamic Instructions Function
async def my_dynamic_instructions(ctx: RunContextWrapper[Person], agent: Agent):
    if ctx.context.user_type.lower() == "patient":
        return """
        Use simple, everyday language. 
        Avoid complex medical jargon. 
        Explain medical terms in easy words. 
        Be empathetic, supportive, and reassuring. 
        Focus on clarity and comfort.
        """
    elif ctx.context.user_type.lower() == "medical student":
        return """
        Use moderate medical terminology with clear explanations. 
        Provide learning opportunities where possible. 
        Break down complex terms but keep the academic depth. 
        Encourage curiosity and medical understanding.
        """
    elif ctx.context.user_type.lower() == "doctor":
        return """
        Use precise medical terminology, abbreviations, and clinical language. 
        Keep responses concise and professional. 
        Assume full medical knowledge. 
        Focus on diagnosis, treatment plans, and efficiency.
        """
    else:
        return "Default mode: Keep responses clear and informative."

# 🤖 Medical Consultation Agent
medical_agent = Agent(
    name="MedicalConsultationAgent",
    instructions=my_dynamic_instructions,
)

# 🚀 Runner
async def main():
    with trace("Medical Dynamic Instructions"):
        result = await Runner.run(
            medical_agent,
            "Can you explain hypertension?",
            run_config=config,
            context=personOne  # Local context (Patient, Student, Doctor)
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
