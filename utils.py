import os
from together import Together
from fpdf import FPDF
import base64
from datetime import datetime
from dotenv import load_dotenv


def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')



load_dotenv()
api = os.environ['lama_api']

def Model(Message):
    client = Together(base_url="https://api.aimlapi.com/v1", api_key=api)
    response = client.chat.completions.create(
        model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo",
        messages  = Message ,
        max_tokens=300,
    )

    response   =  response.choices[0].message.content 
    return response




current_date = datetime.now().date()

def create_message(image , p_dob , p_name ):
    input_mesage=[
            {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": f''' Generate an X-Ray/MRI report for the attached image . The report should have the following format  :

                            1) Title: **DHA Diagnostic Center** (with big font size)
                            2) Heading: **Imaging Center**\n Khyaban-e-Tufail, \n DHA Ph. 7 ext.
                            3) PATIENT: {p_name}
                                DOB: {p_dob}
                                MR #: ________
                                PHYSICIAN: __________
                                EXAM: Extract X-Ray/MRI information as per the X-Ray image
                                DATE: {current_date}

                            4) Clinical Information
                            5) Contrast
                            6) Technique
                            7) Findings
                            8) Impression''',
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image}",
                            },
                    },
                ],
            }, 
    ]
    return input_mesage




class PDF(FPDF):
    def header(self):
        # Set font for header
        self.set_font("Arial", "B", 12)

    def chapter_title(self, title):
        # Set font for chapter title
        self.set_font("Arial", "B", 12)
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(5)

    def chapter_body(self, body):
        # Set font for body
        self.set_font("Arial", "", 12)
        # Split the text into lines and handle bold formatting
        for line in body.split('\n'):
            if line.startswith("**") and line.endswith("**"):
                # Strip the asterisks and set to bold
                self.set_font("Arial", "B", 12)
                line = line[2:-2].strip()
            else:
                self.set_font("Arial", "", 12)
            self.multi_cell(0, 10, line)
        self.ln()