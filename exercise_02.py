from agents import Agent, RunContextWrapper, Runner, trace
from pydantic import BaseModel
from connection import config
import asyncio
import rich

from dotenv import load_dotenv
load_dotenv()

# ✈️ User Context
class Passenger(BaseModel):
    name: str
    seat_preference: str       # window | aisle | middle | any
    travel_experience: str     # first_time | occasional | frequent | premium

# Example Passenger
passengerOne = Passenger(
    name="Sara",
    seat_preference="window",
    travel_experience="first_time"
)

# 🧠 Dynamic Instructions Function
async def airline_dynamic_instructions(ctx: RunContextWrapper[Passenger], agent: Agent):
    seat = ctx.context.seat_preference.lower()
    exp = ctx.context.travel_experience.lower()

    # Case 1: Window + First-time
    if seat == "window" and exp == "first_time":
        return """
        Emphasize the benefits of a window seat. 
        Mention scenic views during take-off and landing. 
        Reassure about the flying experience, explaining step-by-step in a calm, supportive tone.
        """

    # Case 2: Middle + Frequent
    elif seat == "middle" and exp == "frequent":
        return """
        Acknowledge that the middle seat is less preferred. 
        Suggest strategies like choosing seats near the front/back or early check-in. 
        Offer alternatives like paid upgrades or aisle availability. 
        Keep the tone practical and understanding of frequent travel needs.
        """

    # Case 3: Any + Premium
    elif seat == "any" and exp == "premium":
        return """
        Highlight premium travel experience. 
        Focus on luxury options such as extra legroom, lie-flat seats, lounge access, and priority boarding. 
        Stress the comfort and exclusivity of premium class regardless of seat type.
        """

    # Default fallback
    else:
        return """
        Provide clear, helpful seat booking guidance. 
        Adapt explanation tone based on comfort and travel convenience.
        """

# 🤖 Airline Seat Preference Agent
airline_agent = Agent(
    name="AirlineSeatAgent",
    instructions=airline_dynamic_instructions,
)

# 🚀 Runner
async def main():
    with trace("Airline Dynamic Instructions"):
        result = await Runner.run(
            airline_agent,
            "Can you help me choose the best seat for my trip?",
            run_config=config,
            context=passengerOne  # Local context (seat_preference + travel_experience)
        )
        rich.print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
