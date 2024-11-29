from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from groq import Groq
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY2"))

# Create the LLM definition
def create_llm_definition():
    return ChatGroq(
        model="mixtral-8x7b-32768",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )



def processing_text_to_info(input_text):
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an AI that extracts structured information from text."),
            (
                "human", 
                "Extract the following details from the input text:\n"
                "1. Device Name\n"
                "2. Device Price\n"
                "3. Available Offers (if any)\n"
                "4. Website Name\n\n"
                "Input Text: {input_text}"
            ),
        ]
    )
    llm = create_llm_definition()
    chain = prompt | llm
    result = chain.invoke({"input_text": input_text})
    return result.content



# Flask app
app = Flask(__name__)


@app.route('/analyse_text', methods=['POST'])
def analyse_text():
    data = request.json
    text = data.get('text', '')


    if not text:
        return jsonify({'error': 'Text is required'}), 400

    meta_data={}
    result = processing_text_to_info(text)
    print(result)

    return jsonify({'device_info': result})


@app.route('/check', methods=['POST'])
def check():
    return jsonify({'Output':"LLM analysis Server is Running Successfully"})



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
