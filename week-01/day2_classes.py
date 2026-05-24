# week-01/day2_classes.py
# Topic: Python Classes for AI Development
# Why: Every chatbot, agent, and RAG system you build will be a class

import os
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

# ============================================================
# PART 1: What is a class?
# With a class — clean, reusable, professional
# ============================================================

class AIAssistant:
    """
        A simple AI assistant class.
            
    """

    # __init__ is the constructor - runs automatically when you create the object

    def __init__(self, name:str, role:str):
        #These are the instance variables - each object has its own copy

        self.name = name
        self.role = role
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.conversation_history = []
        self.total_input_tokens = 0
        self.total_output_tokens = 0

        print(f"✅ Assistant '{self.name}' created with role: {self.role} ")


    # A method is just a function that belongs to the class
    # Every method takes a 'self' as the first parameter - always

    def chat(self, user_message:str) -> str:
        """send a message and get a response back"""

        # add user message to history
        # This is how the AI remember - we store every message

        self.conversation_history.append({
            "role":"user",
            "content":user_message
        })

        # Make the API call
        response = self.client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=500,
            system=self.role,
            messages=self.conversation_history
        )

        # Extract the response
        assistant_reply = response.content[0].text

        # Add AI response to history too
        self.conversation_history.append(
            {
                "role":"assistant",
                "content": assistant_reply
            }
        )

        # Track Tokens - cumulative across entire conversation
        self.total_input_tokens += response.usage.input_tokens
        self.total_output_tokens += response.usage.output_tokens

        return assistant_reply
    
    def get_stats(self) -> dict:
        """Return usage stats for this session"""

        return {
            "assistant_name":self.name,
            "messages_exchange":len(self.conversation_history),
            "total_input_tokens":self.total_input_tokens,
            "total_output_tokens":self.total_output_tokens,
            "total_tokens":self.total_input_tokens + self.total_output_tokens
        }
    
    def estimate_cost_usd(self)-> dict:
        """
            Estimate the cost of this session in USD.
            Based on Claude Haiku pricing (as of 2025)
            - Input tokens : $0.80 per million tokens = $0.0000008 per token
            - Output tokens: $4.00 per million tokens = $0.000004 per token

            Why track this ? In production , a 1000 user app can burn
            $500/day if you are not watching token usage carefully
        
        
        """

        INPUT_COST_PER_TOKEN = 0.80 / 1000000
        OUTPUT_COST_PER_TOKEN = 4.00 /1000000

        input_cost = self.total_input_tokens * INPUT_COST_PER_TOKEN
        output_cost = self.total_output_tokens * OUTPUT_COST_PER_TOKEN
        total_cost = input_cost + output_cost
        return {
            "model"           : "claude-haiku-4-5-20251001",
            "input_tokens"    : self.total_input_tokens,
            "output_tokens"   : self.total_output_tokens,
            "input_cost_usd"  : round(input_cost,8),
            "output_cost_usd" : round(output_cost, 8),
            "total_cost_usd"  : round(total_cost, 8),
            "total_cost_inr"  : round(total_cost * 84, 6)
        }
    
    def reset(self):
        """Clear conversation history and reset token counters to zero"""
        self.conversation_history = []
        self.total_input_tokens = 0    # ← reset cost tracking too
        self.total_output_tokens = 0   # ← otherwise cost is misleading
        print(f"🔄 Conversation history cleared for '{self.name}'")


# ============================================================
# PART 2: Creating objects from the class
# One class → multiple independent objects
# ============================================================

# Create two completely separate assistants from the SAME class

python_tutor = AIAssistant(
    name="PyTutor",
    role="You are an expert Python Tutor. Give short , clear explanation with example"
)

career_coach = AIAssistant(
    name="CareerCoach",
    role="You are GenAI career coach for Indian IT professionals, Be direct and practical."

)

# Each object has its OWN conversation history — completely separate
print("\n---- Talking to Python Tutor")
reply1 = python_tutor.chat("What is the difference between a list and a tuple in Python?")
print(f"PyTutor: {reply1}")

print("\n----- Talking to Career Coach")
reply2 = career_coach.chat("I have 7 years of SAS mainframe experience. How valuable is that for GenAI roles?")
print(f"CareerCoach: {reply2}")

# Python tutor has NO idea about the career conversation — separate objects!
print("\n--- Continuing with Python Tutor ---")
reply3 = python_tutor.chat("Can you give me an example of when to use each?")
print(f"PyTutor: {reply3}")
# Notice: it remembers we were talking about lists vs tuples!

# Print stats and cost for each
print(f"\n📊 Session Stats + Cost Estimate: ")

for assistant in [python_tutor, career_coach]:
    stats = assistant.get_stats()
    cost = assistant.estimate_cost_usd()

    print(f"\n🤖 Assistant  : {stats['assistant_name']}")
    print(f"  Messages      : {stats['messages_exchange']}")
    print(f"  Input tokens  : {cost['input_tokens']}")
    print(f"  Output Tokens : {cost['output_tokens']}")
    print(f"  Total Tokens  : {stats['total_tokens']}")
    print(f"  Cost(USD)     : ${cost['total_cost_usd']}")
    print(f"  Cost(INR)     : ₹{cost['total_cost_inr']}")

# Test the reset method
print("\n--- Testing Reset ---")
print(f"Before reset - history length: {len(python_tutor.conversation_history)}")
python_tutor.reset()
print(f"After reset - history length: {len(python_tutor.conversation_history)}")

