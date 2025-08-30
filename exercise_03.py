from agents import Agent, RunContextWrapper, Runner, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich

from dotenv import load_dotenv
load_dotenv()

# 🌍 User Context
class Traveler(BaseModel):
    name: str
    trip_type: str            # adventure | cultural | business
    traveler_profile: str     # solo | family | executive | medical_student | doctor

# Example Traveler
travelerOne = Traveler(
    name="Hamza",
    trip_type="adventure",
    traveler_profile="solo"
)

# 🧠 Dynamic Instructions Function
async def travel_dynamic_instructions(ctx: RunContextWrapper[Traveler], agent: Agent):
    trip = ctx.context.trip_type.lower()
    profile = ctx.context.traveler_profile.lower()

    # Case 1: Adventure + Solo
    if trip == "adventure" and profile == "solo":
        return """
        Suggest exciting adventure activities such as hiking, scuba diving, or mountain biking. 
        Emphasize safety tips for solo travelers. 
        Recommend social hostels, backpacker communities, and group tours to meet new people. 
        Keep the tone encouraging and adventurous.
        """

    # Case 2: Cultural + Family
    elif trip == "cultural" and profile == "family":
        return """
        Focus on cultural and educational attractions. 
        Recommend kid-friendly museums, heritage sites with interactive experiences, and cultural shows. 
        Suggest family accommodations with comfort, safety, and amenities. 
        Use a warm and family-oriented tone.
        """

    # Case 3: Business + Executive
    elif trip == "business" and profile == "executive":
        return """
        Emphasize business efficiency. 
        Recommend hotels near airports or city centers with business facilities. 
        Highlight services like reliable Wi-Fi, conference rooms, premium lounges, and fast check-in. 
        Keep the tone concise, professional, and executive-friendly.
        """

    # Case 4: Medical Student
    elif profile == "medical_student":
        return """
        Use moderate medical terminology with simple explanations. 
        Recommend affordable accommodations near universities, libraries, and cultural learning sites. 
        Suggest opportunities for networking, conferences, and study-friendly cafes. 
        Keep the tone academic but supportive.
        """

    # Case 5: Doctor
    elif profile == "doctor":
        return """
        Use professional and concise medical terminology where appropriate. 
        Recommend premium hotels with wellness facilities, spas, and fast connectivity. 
        Highlight destinations with world-class healthcare infrastructure in case of emergencies. 
        Emphasize relaxation, efficiency, and high-standard amenities.
        """

    # Default fallback
    else:
        return """
        Provide clear travel recommendations tailored to comfort, safety, and enjoyment. 
        Adapt suggestions based on trip purpose and traveler needs.
        """

# 🤖 Travel Planning Agent
travel_agent = Agent(
    name="TravelPlanningAgent",
    instructions=travel_dynamic_instructions,
)

# 🚀 Runner
async def main():
    with trace("Travel Dynamic Instructions"):
        result = await Runner.run(
            travel_agent,
            "Can you suggest the best travel plan for me?",
            run_config=config,
            context=travelerOne  # Local context (trip_type + traveler_profile)
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
