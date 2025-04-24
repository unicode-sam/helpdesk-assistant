from google import genai
from google.genai import types
import base64
from prompts.prompt import ticketDetail_prompt,transcript_prompt,call_analysis_prompt
import json
import os

# If you're using a service account key file:
SERVICE_ACCOUNT_KEY_PATH = os.getenv('SERVICE_ACCOUNT_KEY_PATH')
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = SERVICE_ACCOUNT_KEY_PATH

# If you're using an API key instead, set it like this:
# os.environ['API_KEY'] = os.getenv('API_KEY')

PROJECT = os.getenv('GCP_PROJECT_NAME')
PROJECT_ID = os.getenv('GCP_PROJECT_ID')
LOCATION = os.getenv('GCP_LOCATION', 'us-central1')  # Default to 'us-central1' if not set

class Model:
    def __init__(self):
        self.client = genai.Client(
        vertexai=True,
        project="gbg-neuro",
        location="us-central1",
        )
        self.model = "gemini-2.0-flash-001"

        self.generate_content_config = types.GenerateContentConfig(
        temperature = 0,
        top_p = 1,
        max_output_tokens = 8192,
        response_modalities = ["TEXT"],
        safety_settings = [types.SafetySetting(
        category="HARM_CATEGORY_HATE_SPEECH",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_DANGEROUS_CONTENT",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
        threshold="OFF"
        ),types.SafetySetting(
        category="HARM_CATEGORY_HARASSMENT",
        threshold="OFF"
        )],
    )

    def transcript(self,conv):
        prompt=transcript_prompt+conv
        contents = [
            types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt)
            ]
            ),
        ]
        
        response=""
        for chunk in self.client.models.generate_content_stream(
            model = self.model,
            contents = contents,
            config = self.generate_content_config,
            ):
            response+=chunk.text
        print(response)
        return response

    def call_analysis(self,transcript):
        prompt=call_analysis_prompt+transcript
        contents = [
            types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt)
            ]
            ),
        ]
        
        response=""
        for chunk in self.client.models.generate_content_stream(
            model = self.model,
            contents = contents,
            config = self.generate_content_config,
            ):
            response+=chunk.text
        
        response=response.replace("\n","")
        try:
            response=response.replace("    ","")
        except:
            pass
        # print(response)
        cleaned_response=response.strip("```json").strip("```")
        cleaned_response=cleaned_response.strip()
        # print(cleaned_response)
        data_dict=json.loads(cleaned_response)

        intent=data_dict.get("intent")
        summary=data_dict.get("summary")
        sentiment=data_dict.get("sentiment")
        suggestion=data_dict.get("suggestion")
        status=data_dict.get("status")

        print("Intent:\t",intent)
        print("Summary:\t",summary)
        print("Sentiment:\t",sentiment)
        print("suggestion:\t",suggestion)
        print("Status:\t",status)

        return intent,summary,sentiment,suggestion,status


