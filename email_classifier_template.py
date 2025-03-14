# Configuration and imports
import os
import json
import pandas as pd
from typing import Dict, List, Optional, Tuple
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Sample email dataset
sample_emails = [
    {
        "id": "001",
        "from": "angry.customer@example.com",
        "subject": "Broken product received",
        "body": "I received my order #12345 yesterday but it arrived completely damaged. This is unacceptable and I demand a refund immediately. This is the worst customer service I've experienced.",
        "timestamp": "2024-03-15T10:30:00Z"
    },
    {
        "id": "002",
        "from": "curious.shopper@example.com",
        "subject": "Question about product specifications",
        "body": "Hi, I'm interested in buying your premium package but I couldn't find information about whether it's compatible with Mac OS. Could you please clarify this? Thanks!",
        "timestamp": "2024-03-15T11:45:00Z"
    },
    {
        "id": "003",
        "from": "happy.user@example.com",
        "subject": "Amazing customer support",
        "body": "I just wanted to say thank you for the excellent support I received from Sarah on your team. She went above and beyond to help resolve my issue. Keep up the great work!",
        "timestamp": "2024-03-15T13:15:00Z"
    },
    {
        "id": "004",
        "from": "tech.user@example.com",
        "subject": "Need help with installation",
        "body": "I've been trying to install the software for the past hour but keep getting error code 5123. I've already tried restarting my computer and clearing the cache. Please help!",
        "timestamp": "2024-03-15T14:20:00Z"
    },
    {
        "id": "005",
        "from": "business.client@example.com",
        "subject": "Partnership opportunity",
        "body": "Our company is interested in exploring potential partnership opportunities with your organization. Would it be possible to schedule a call next week to discuss this further?",
        "timestamp": "2024-03-15T15:00:00Z"
    }
]



class EmailProcessor:
    def __init__(self):
        """Initialize the email processor with OpenAI API key."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Define valid categories
        self.valid_categories = {
            "complaint", "inquiry", "feedback",
            "support_request", "other"
        }

    def classify_email(self, email: Dict) -> Optional[str]:
        """
        Classify an email using LLM.
        Returns the classification category or None if classification fails.
        
        TODO: 
        1. Design and implement the classification prompt
        2. Make the API call with appropriate error handling
        3. Validate and return the classification
        """
     
        messages=[
                {
                    "role": "user",
                    "content": "You're an AI assistant tasked with classifying emails."
                },{
                    "role": "user",
                    "content": f"""
                                
                                Classify the email using the following categories:
                                - complaint
                                - inquiry
                                - feedback
                                - support_request
                                - other
                
                                Email:
                                ---
                                Subject: {email.get('subject', 'No subject')}
                                Body: {email.get('body', 'No body')}
                                ---
                
                                Respond with the category name only, as written above
                                """
                }
            ]

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=5,
                temperature=0
            )
            
            classification = completion.choices[0].message.content.strip().lower()
            if classification in self.valid_categories:
                return classification
            else:
                logger.error(f"The classification the model gave is not on the valid list - {classification}")
                return "other"
                
        except Exception as e:
            logger.error(f"There was an error classifying the email {e}")
            return None

    def generate_response(self, email: Dict, classification: str) -> Optional[str]:
        """
        Generate an automated response based on email classification.
        
        TODO:
        1. Design the response generation prompt
        2. Implement appropriate response templates
        3. Add error handling
        """

        

        messages=[
                        {
                            "role": "user",
                            "content": "You're an AI assistant tasked with responding to emails."
                        },{
                            "role": "user",
                            "content": f"""
                                        
                                       Given the following classification as {classification}
                                    
                        
                                        And the following email:
                                        ---
                                        Subject: {email.get('subject', 'No subject')}
                                        Body: {email.get('body', 'No body')}
                                        ---
                        
                                        Write an email response to send to the user. Be polite, professional and service focused.

                                        Don't add commments.
                                        Don't add placeholder text, call the receiver "you" or similar. Don't put any placeholder text like "[recipient's name]"
                                        write a generic email. You're an AIlia Assire, a Proffesional problem solver for company A. Sign the email with that
                                        
                                        """
                        }
         ]

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
               
                temperature=0
            )
            
            email = completion.choices[0].message.content
         
            logger.info(f"The email body is: {email}")

            return email
            
                
        except Exception as e:
            logger.error(f"There was an error classifying the email {e}")
            return None


        
class EmailAutomationSystem:
    def __init__(self, processor: EmailProcessor):
        """Initialize the automation system with an EmailProcessor."""
        self.processor = processor
        self.response_handlers = {
            "complaint": self._handle_complaint,
            "inquiry": self._handle_inquiry,
            "feedback": self._handle_feedback,
            "support_request": self._handle_support_request,
            "other": self._handle_other
        }

    def process_email(self, email: Dict) -> Dict:
        """
        Process a single email through the complete pipeline.
        Returns a dictionary with the processing results.
        
        TODO:
        1. Implement the complete processing pipeline
        2. Add appropriate error handling
        3. Return processing results
        """
        processor=EmailProcessor()
        classification = processor.classify_email(email)
        try:
            response = self.response_handlers[classification](email)
            return [email.get('id', '0001'), 'yes', classification, response]
        except:
            return [email.get('id', '0001'), 'no', classification, '']
            
       

        

    def _handle_complaint(self, email: Dict):
        """
        Handle complaint emails.
        TODO: Implement complaint handling logic
        """
        try:
            processor=EmailProcessor()
            response =processor.generate_response(email=email, classification="complaint")
            send_complaint_response( email.get('id', '0001'), response)
            create_urgent_ticket(email.get('id', '0001'), 'complaint', email.get('body', 'No email body'))
    
        
            return  response
        except:
            return ''
        
    def _handle_inquiry(self, email: Dict):
        """
        Handle inquiry emails.
        TODO: Implement inquiry handling logic
        """
        try:
            processor=EmailProcessor()
            response = processor.generate_response(email=email, classification="inquiry")
            send_standard_response( email.get('id', '0001'), response)
            return response
        except:
            return  ''



    def _handle_feedback(self, email: Dict):
        """
        Handle feedback emails.
        TODO: Implement feedback handling logic
        """
        try:
            processor=EmailProcessor()
            response =processor.generate_response(email=email, classification="feedback")
            log_customer_feedback( email.get('id', '0001'), email.get('body', 'No feedback'))
            send_standard_response( email.get('id', '0001'), response)
            return  response
        except:
            return  ''


    def _handle_support_request(self, email: Dict):
        """
        Handle support request emails.
        TODO: Implement support request handling logic
        """
        try:
            processor=EmailProcessor()
            response = processor.generate_response(email=email, classification="support_request")
            create_support_ticket( email.get('id', '0001'), context =  email.get('body', 'No email body'))
            return  response
        except:
            return  ''

    def _handle_other(self, email: Dict):
        """
        Handle other category emails.
        TODO: Implement handling logic for other categories
        """
        try:
            processor=EmailProcessor()
            response = processor.generate_response(email=email, classification="other")
            send_standard_response( email.get('id', '0001'), response)      
            return  response
        except:
            return ''



# Mock service functions
def send_complaint_response(email_id: str, response: str):
    """Mock function to simulate sending a response to a complaint"""
    logger.info(f"Sending complaint response for email {email_id}")
    # In real implementation: integrate with email service


def send_standard_response(email_id: str, response: str):
    """Mock function to simulate sending a standard response"""
    logger.info(f"Sending standard response for email {email_id}")
    # In real implementation: integrate with email service


def create_urgent_ticket(email_id: str, category: str, context: str):
    """Mock function to simulate creating an urgent ticket"""
    logger.info(f"Creating urgent ticket for email {email_id}")
    # In real implementation: integrate with ticket system


def create_support_ticket(email_id: str, context: str):
    """Mock function to simulate creating a support ticket"""
    logger.info(f"Creating support ticket for email {email_id}")
    # In real implementation: integrate with ticket system


def log_customer_feedback(email_id: str, feedback: str):
    """Mock function to simulate logging customer feedback"""
    logger.info(f"Logging feedback for email {email_id}")
    logger.info(f" {feedback}")

    # In real implementation: integrate with feedback system


def run_demonstration():
    """Run a demonstration of the complete system."""
    # Initialize the system
    processor = EmailProcessor()
    automation_system = EmailAutomationSystem(processor)

    # Process all sample emails
    results = []
    for email in sample_emails:
        logger.info(f"\nProcessing email {email['id']}...")
        result = automation_system.process_email(email)
        results.append(result)

    # Create a summary DataFrame
    df = pd.DataFrame(results, columns=["email_id", "success", "classification", "response_sent"])
    print("\nProcessing Summary:")
    print(df[["email_id", "success", "classification", "response_sent"]])

    return df


# Example usage:
if __name__ == "__main__":
    results_df = run_demonstration()    
