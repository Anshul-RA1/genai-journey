# week-01/day2_typehints.py
# Topic: Type Hints for AI Development
# Why: LangChain, FastAPI, Pydantic ALL require this syntax

# ============================================================
# PART 1: Basic Type Hints
# ============================================================

# Format: variable_name: type = value
name: str = "Anshul"
experience: int = 7
salary: float = 25.5
is_learning: bool = True

print("=== Basic Types ===")
print(f"Name            : {name}         : type : {type(name)}")
print(f"Experience      : {experience}   : type : {type(experience)}")
print(f"Salary          : {salary}       : type : {type(salary)}")
print(f"Learning        : {is_learning}  : type : {type(is_learning)}")

# ============================================================
# PART 2: Type Hints in Functions
# ============================================================

# parameter: type   → what goes IN
# -> type           → what comes OUT

def greet_engineer(name: str, years: int) -> str:
    """Takes a name and years, returns a greeting string"""
    return f"Hello {name}! you have {years} years of experience"

def calculate_token_cost(
        input_tokens: int,
        output_tokens: int,
        input_rate: float = 0.80,
        output_rate: float = 4.00
) -> dict:
    """Calculate API cost - same logic as our AIAssistant Class"""
    input_cost = (input_tokens/1000000) * input_rate
    output_cost = (output_tokens/1000000) * output_rate
    total_cost = input_cost + output_cost

    return {
        "input_cost_usd" : round(input_cost,8),
        "output_cost_usd": round(output_cost,8),
        "total_cost_usd" : round(total_cost, 8),
        "total_cost_inr" : round(total_cost* 88 , 8)
    }

print("\n=== Functions with Type Hints ===")
greeting = greet_engineer("Anshul", 7)
print(greeting)

cost = calculate_token_cost(input_tokens=500, output_tokens=800)
print(f"USD_Cost: ${cost['total_cost_usd']}, INR_Cost: ₹{cost['total_cost_inr']}")


# ============================================================
# PART 3: typing module — for complex types
# This is what LangChain uses EVERYWHERE
# ============================================================

from typing import Optional, List, Dict, Tuple, Union
# List[type] -> a list where evy item is that type 

def process_skills(skills: List[str]) -> List[str]:
    """Takes list of skills , return them uppercase"""
    return [skill.upper() for skill in skills]


# Dict[key_type, value_type] -> a disctionary with specific key/value types
def build_message(role:str, content:str) -> Dict[str, str]:
    """Build an API message dict - you have been writting these all day"""
    return {
        "role":role, 
        "content":content
    }     

# Optional[type] -> can be that type or None
# This is extremely common in AI functions

def create_assistant(
        name: str,
        role: str,
        model: Optional[str] = None
) -> Dict[str, str]:
    """Create assistant config - model is optional"""
    if model is None:
        model = "claude-haiku-4-5-20251001"
    return {
        "name":name,
        "role":role,
        "model": model
    }

# Union[type1, type2] -> can be EITHER type
# Common when AI returns text or a structured object

def parse_response(response: Union[str,dict]) -> str:
    """Handle response whether it's a string or dict"""
    if isinstance(response, dict):
        return response.get("content","")
    return response

print("\n=== Complex Types from typing module ===")

skills = process_skills(["SAS", "Python", "Power BI"])
print(f"Skills uppercased: {skills}")

message = build_message("user", "Hello Claude")
print(f"Message built : {message}")

assistant1 = create_assistant("PyTutor","Python expert")
assistant2 = create_assistant("CodeBot", "Code reviewer", model = "claude-sonnet-4-6")

print(f"Assistant 1 model : {assistant1['model']}")  # uses default
print(f"Assistant 2 model : {assistant2['model']}")  # uses provided

print(f"Parse string      : {parse_response('hello')}")
print(f"Parse dict        : {parse_response({'content': 'hi there'})}")

# ============================================================
# PART 4: Pydantic — Type Hints on steroids
# Used heavily in LangChain, FastAPI
# Validates data automatically — crashes early with clear errors
# ============================================================

from pydantic import BaseModel, Field

# A pydantic model is a class where every field has a type
# Pydantic VALIDATES THE TYPES WHEN YOU CREATE OBJECT.

class ChatMessage(BaseModel):
    """Represents a single message in a conversation"""
    role : str
    content : str
    tokens : Optional[int] = None

class AssistantConfig(BaseModel):
    """Configuration for an AI assistant"""
    name        : str
    role        : str
    model       : str = "claude-haiku-4-5-20251001"
    max_tokens  : int = 500
    temperature : float = Field(default = 0.7, ge=0, le=1.0)
    
print("\n=== Pydantic Models ===")

#Create a valid message
msg = ChatMessage(role="user", content="Hello!", tokens=10)
print(f"Message : {msg}")
print(f"Role : {msg.role}")
print(f"Tokens : {msg.tokens}")

# create assistant config

config = AssistantConfig(name="PyTutor", role="Python expert")
print(f"\nConfig  : {config}")
print(f"Model   : {config.model}")
print(f"Temp : {config.temperature}")

# Pydantic auto-converts compatible types
config2 = AssistantConfig(
    name="CodeBot",
    role="Code reviewer",
    temperature=0.3  # overrides default
)


print(f"\nCodeBot temp: {config2.temperature}")

# Pydantic catches wrong types immediately with clear error
print("\n=== Pydantic Validation (catching bad data) ===")
try:
    bad_config = AssistantConfig(
        name="BadBot",
        role="Tester",
        temperature=5.0  #violates le=1.0 rule
    )
except Exception as e:
    print(f"Pydantic caught bad data : temperature = 5.0 is invalid")
    print(f" Error: {e}")


# Convert Pydantic model to dict (useful for APIs)
config_dict=config.model_dump()
print(f"\nAs dict: {config_dict}")