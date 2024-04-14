from openai import OpenAI
from helper import get_transcript_from_link
import json
from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)


api_key = "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"
client = OpenAI(api_key = api_key)
model = "gpt-3.5-turbo"



@app.route('/getanswers/<video_link>/<int:number>/<difficulty_selected>', methods=['GET'])
def return_answers(video_link:str, number:int, difficulty_selected:str):
    number_of_questions = number 
    difficulty = difficulty_selected

    transcript = get_transcript_from_link(video_link)

    if transcript != "Error":


        the_prompt = f"""

    Given this transcript from an educational academic youtube video:
    {transcript}

    Generate me {number_of_questions} multiple choice questions with 5 options of {difficulty} difficulty for all the topics in the video.
    Make sure the questions are only about the academic topics covered in the video and nothing else.


    Also return this reponse in a json format so I can json.loads into python easily. 
    The format of the json object should be a list of each question. Within each question,
    there should be the options where each option should be given a flag True or False. True if its the correct answer and False if its not.
    It should also contain the reason for being right/wrong respectively.

    """
        ai_magic = client.chat.completions.create(
        model = model,
        messages = [
            {"role": "system", "content": "You are the world's best teacher"},
            {"role": "user", "content": the_prompt}
            ]
    )
        response = ai_magic.choices[0].message.content
        response = response[response.find('[') : response.rfind(']') + 1]

        data = json.loads(response)

        return {"response": data}

    else:
        return {"response": ["Error"]}
    

if __name__ == "__main__":
    app.run(debug = True)