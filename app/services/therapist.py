import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# Securely fetch the API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set.")

genai.configure(api_key=api_key)

# ... (rest of your code remains the same for now)
system_instruction = """
You are an empathetic, non-judgmental virtual listener and supportive chat companion. 
Your goal is to provide emotional support and a safe space for users to vent anonymously.
Guidelines:
1. Validate the user's feelings.
2. Ask gentle, open-ended questions to help them reflect.
3. Keep responses concise and conversational (1 to 3 sentences).
4. Do not offer medical advice, diagnose conditions, or pretend to be a licensed human therapist.
"""

# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-3.5-flash",
    system_instruction=system_instruction
)

import asyncio
# ... (keep the imports and model initialization exactly as they are) ...

class TherapistChat:
    """An isolated AI therapist session that remembers conversation history."""
    
    def __init__(self):
        self.chat_session = model.start_chat(history=[])

    async def get_response(self, user_message: str) -> str:
        lower_msg = user_message.lower()
        if "suicide" in lower_msg or "kill myself" in lower_msg or "end my life" in lower_msg:
            return (
                "This sounds incredibly painful, and I want you to know you are not alone. "
                "Please reach out to someone who can help right now. You can call the "
                "AASRA helpline at 9820466726, contact emergency services at 112, or go to "
                "your nearest hospital. Your life has value, and there is support available."
            )

        try:
            # --- THE ASYNC UPGRADE ---
            # Offload the blocking network call to a separate thread
            response = await asyncio.to_thread(
                self.chat_session.send_message, 
                user_message
            )
            return response.text
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return "I'm having a little trouble processing right now. Could you tell me more about what you're feeling?"