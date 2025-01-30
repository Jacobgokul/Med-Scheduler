import os
import json
import ast
import traceback
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from langchain.memory import ConversationBufferMemory
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

from database.database import engine, get_db
from database.models import Base, Appointment


load_dotenv() # Load API key from .env
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise Exception("Kindly create and add OpenAI key in .env file")

Base.metadata.create_all(engine)

app = FastAPI()

# Define Prompt
prompt_template = PromptTemplate(
    input_variables=["chat_history", "user_message"],
    template="""
    You are a hospital appointment scheduler. Your job is to collect the following details from the user:
    
    - Doctor's specialty (e.g., Dentist, Cardiologist) or problem
    - Appointment date (YYYY-MM-DD) else convert to this format
    - Appointment time (HH:MM) else convert to this format

    If user provides problem suggest suitable doctor

    If any information is missing, ask follow-up questions to collect it.

    If all details are collected, respond with dict format:
    {{
        "doctor": "Doctor's Name",
        "date": "YYYY-MM-DD",
        "time": "HH:MM"
    }}

    If user needs to provide more info response with dict format:
    {{
        "info_required": "" //Ask user for missing details
    }}

    Conversation History:
    {chat_history}

    User: {user_message}
    """
)

llm = ChatOpenAI(model_name="gpt-4o", openai_api_key=openai_key)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

conversation = LLMChain(
    llm=llm,
    prompt=prompt_template,
    memory=memory
)

@app.post("/chat")
def chat_with_bot(user_message: str, db: Session = Depends(get_db)):
    """
    AI-driven chatbot that interacts with users to book or cancel an appointment.
    """
    try:
        response = conversation.run(user_message)

        print(response)
        if 'json' in response:
            response = response[7:-3]
        
        try:
            extracted_info = eval(response)
        except:
            return {"response": "I couldn't understand your request. Can you rephrase?"}

        if "info_required" in extracted_info:
            return {"response": extracted_info["info_required"]}

        doctor = extracted_info.get("doctor")
        date = extracted_info.get("date")
        time = extracted_info.get("time")

        if "cancel" in user_message.lower():  # Handle cancel request
            appointment_to_cancel = db.query(Appointment).filter_by(
                doctor_name=doctor, 
                appointment_date=f"{date} {time}",
                status="Scheduled"
            )
            
            if appointment_to_cancel.first():
                appointment_to_cancel.update({
                    "status": "Cancelled"
                })
                db.commit()
                memory.clear()
                return {"response": f"Your appointment with {doctor} on {date} at {time} has been successfully cancelled."}
            else:
                return {"response": "No appointment found to cancel at the specified time."}

        existing = db.query(Appointment).filter_by(doctor_name=doctor, appointment_date=f"{date} {time}", status="Scheduled").first()

        if existing:
            return {"response": "That slot is already booked. Please choose another time."}

        new_appointment = Appointment(patient_name="User", doctor_name=doctor, appointment_date=f"{date} {time}")
        db.add(new_appointment)
        db.commit()

        memory.clear()
        return {"response": f"Your appointment with {doctor} is confirmed on {date} at {time}!"}

    except Exception as e:
        traceback.print_exc()
        return {"response": "Please try again"}
