import asyncio
import os
from dotenv import load_dotenv
import aiohttp

load_dotenv()
API_KEY = os.getenv("API_KEY")

async def prompts() -> list:
    heros = """
    Give me the list of all 10 top highest win rate Dota 2 hero 2023
    """

    players = """
    Top players in the game Dota 2 in 2023
    """

    team = """
    Give me the name the name of all team who got directe invite in TI 2023 dota 2.
    """
    
    return [heros, players, team ]

async def fetch_ai_response(session, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    async with session.post(url, headers=headers, json=payload) as response:
        result = await response.json()
        # Extract text from the response
        try:
            content = result['candidates'][0]['content']['parts'][0]['text']
            return content
        except (KeyError, IndexError) as e:
            # Log the error and response for debugging
            print(f"Error parsing response: {e}")
            print(f"Unexpected response format: {result}")
            return "Error: Unexpected response format"

async def test_questions_from_ai() -> list:
    prompts_list = await prompts()
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_ai_response(session, prompt) for prompt in prompts_list]
        results = await asyncio.gather(*tasks)
    return results

if __name__ == "__main__":
    responses = asyncio.run(test_questions_from_ai())
    for inx, response in enumerate(responses):
        print(f"Response: {inx} ", response)