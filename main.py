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
    """
    Sends a POST request to the Google Generative Language API to generate content based on the given prompt.
    
    Args:
        session (aiohttp.ClientSession): An instance of the aiohttp ClientSession class.
        prompt (str): The prompt to generate content for.
    
    Returns:
        str: The generated content.
    
    Raises:
        None
    
    Notes:
        This function sends a POST request to the Google Generative Language API endpoint.
        The request includes the prompt in the request payload.
        The response from the API is parsed to extract the generated content.
        If the response format is unexpected, an error message is returned.
    """
    # Construct the URL for the API endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    
    # Set the headers for the request
    headers = {
        "Content-Type": "application/json"
    }
    
    # Construct the request payload
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
    
    # Send the POST request to the API endpoint
    async with session.post(url, headers=headers, json=payload) as response:
        # Parse the response from the API
        result = await response.json()
        
        # Extract the generated content from the response
        try:
            content = result['candidates'][0]['content']['parts'][0]['text']
            return content
        except (KeyError, IndexError) as e:
            # Log the error and the response for debugging purposes
            print(f"Error parsing response: {e}")
            print(f"Unexpected response format: {result}")
            
            # Return an error message if the response format is unexpected
            return "Error: Unexpected response format"



# This function takes a list of prompts and uses the fetch_ai_response function to retrieve the AI response for each prompt.
# The function then uses asyncio.gather to run the fetch_ai_response function in parallel for each prompt.
# The results are returned as a list of responses.

async def test_questions_from_ai() -> list:
    # Get the list of prompts from the prompts function
    prompts_list = await prompts()
    
    # Create an instance of the aiohttp ClientSession class
    async with aiohttp.ClientSession() as session:
        # Create a list of tasks to run the fetch_ai_response function for each prompt
        tasks = [fetch_ai_response(session, prompt) for prompt in prompts_list]
        
        # Run the tasks in parallel and wait for all of them to complete
        results = await asyncio.gather(*tasks)
    
    # Return the list of responses
    return results

if __name__ == "__main__":
    responses = asyncio.run(test_questions_from_ai())
    for inx, response in enumerate(responses):
        print(f"Response: {inx} ", response)