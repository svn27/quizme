from openai import OpenAI
from helper import get_transcript_from_link
import json
from flask import Flask
from flask_cors import CORS
import os


app = Flask(__name__)
CORS(app)


api_key = os.environ['my_openai_secretkey']
client = OpenAI(api_key = api_key)
model = "gpt-4"
format = {
    "1": {
        "question": "Question 1",
        "a": [
            {"option a": [True, "reason why option is correct"]},
            {"option b": [False, "reason why option is wrong"]},
            {"option c": [False, "reason why option is wrong"]},
            {"option d": [False, "reason why option is wrong"]}
        ]
    },
    "2": {
        "question": "Question 2",
        "a": [
            {"option a": [True, "reason why option is correct"]},
            {"option b": [False, "reason why option is wrong"]},
            {"option c": [False, "reason why option is wrong"]},
            {"option d": [False, "reason why option is wrong"]}
        ]
    },
    "3": {
        "question": "Question 3",
        "a": [
            {"option a": [True, "reason why option is correct"]},
            {"option b": [False, "reason why option is wrong"]},
            {"option c": [False, "reason why option is wrong"]},
            {"option d": [False, "reason why option is wrong"]}
        ]
    }
}


@app.route('/getanswers/<video_link>/<int:number>/<difficulty_selected>', methods=['GET'])
def return_answers(video_link:str, number:int, difficulty_selected:str):
    number_of_questions = number 
    difficulty = difficulty_selected

    transcript = get_transcript_from_link(video_link)

    if transcript != "Error":


        the_prompt = f"""

    Given this transcript from an educational academic youtube video:
    {transcript}

    Generate me 5 multiple choice questions with 4 options of {difficulty} difficulty for all the topics in the video.
    Make sure the questions are only about the academic topics covered in the video and nothing else.
    Do NOT leave the json object unfinished, if a question won't fit within the 2000 word limit, then skip the question and neatly close the json object.

    Also return this reponse in a json format so I can json.loads into python easily. 
    The format of the json object should be the same as this format. Make sure the booleans used in the output are lowercase i.e true and false, not True or False.
    {format}
    
  
    """
        ai_magic = client.chat.completions.create(
        model = model,
        messages = [
            {"role": "system", "content": "You are the world's best teacher"},
            {"role": "user", "content": the_prompt}
            ]
    )
        response = ai_magic.choices[0].message.content
        response = response.replace("True", "true")
        response = response.replace("False", "false")
        print(response)
        print("________")
        data = json.loads(response)
        print("###################################")
        print(data)

        return {"response": data}

    else:
        return {"response": ["Error"]}



# @app.route('/getanswers/<video_link>/<int:number>/<difficulty_selected>', methods=['GET'])
# def return_answers(video_link:str, number:int, difficulty_selected:str):
#     response = """
#     {
#         "1": {
#             "question": "What does the double integral of a scalar field over a region in the plane represent?",
#             "a": [
#                 {
#                     "The area enclosed by the curve defined by the scalar field in the xy-plane": [false, "The double integral of a scalar field calculates the volume, not the area."]
#                 },
#                 {
#                     "The volume under the surface defined by the scalar field over that region": [true, "The volume under the surface given by the scalar field across the specified area in the plane is calculated by the double integral."]
#                 },
#                 {
#                     "The length of the curve defined by the scalar field in the xyz-space": [false, "The double integral calculates the volume under a surface, not the length of a curve."]
#                 },
#                 {
#                     "The area of the smallest rectangle that can contain the region in the plane": [false, "The smallest rectangle enclosing a region is not represented by a double integral of a scalar field."]
#                 }
#             ]
#         },
#         "2": {
#             "question": "What property justifies the ability to separate a double integral over a rectangular region into two separate single integrals?",
#             "a": [
#                 {
#                     "Linearity": [true, "The ability to separate integrals is a result of linearity, which allows the integration of sums and differences of functions to be split."]
#                 },
#                 {
#                     "Order": [false, "The order property pertains to the relationship between integral limits and does not govern the separation of integrals."]
#                 },
#                 {
#                     "Domain Splitting": [false, "The domain splitting rule applies when the space of integration can be split into distinct areas, not when integrals can be separated."]
#                 },
#                 {
#                     "Binding": [false, "There is no property known as 'Binding' in this context."]
#                 }
#             ]
#         },
#         "3": {
#             "question": "In general, does the order of integration matter when conducting double integrals?",
#             "a": [
#                 {
#                     "Yes, it always matters": [false, "For certain functions that are bounded and continuous on a rectangular domain, the order doesn't change the result."]
#                 },
#                 {
#                     "Yes, but only for unbounded functions": [false, "The order can also affect bounded functions on complex domains."]
#                 },
#                 {
#                     "No, it never matters": [false, "The order can affect the result for unbounded functions or when the domain is not a rectangle."]
#                 },
#                 {
#                     "No, but only for continuous, bounded functions on a rectangular domain": [true, "If the function is bounded and continuous and the domain is rectangular, the order of integration doesn't impact the result."]
#                 }
#             ]
#         },
#         "4": {
#             "question": "What is the initial step when considering to integrate with respect to 'X' then 'Y' on a complex domain?",
#             "a": [
#                 {
#                     "Divide the domain into horizontal slivers": [true, "When integrating first with respect to 'X' and then 'Y', we consider the domain split into horizontal slivers."]
#                 },
#                 {
#                     "Divide the domain into vertical slivers": [false, "Dividing the domain into vertical slivers is considered when integrating first with respect to 'Y' and then 'X'."]
#                 },
#                 {
#                     "Determine the limits of 'Y'": [false, "Although determining the limits factors in later, the initial step involves thinking of the domain in slivers, not defining the limits."]
#                 },
#                 {
#                     "Calculate the Jacobian determinant": [false, "The Jacobian determinant is used in coordinate transformations, not in defining the initial approach to integration order."]
#                 }
#             ]
#         },
#         "5": {
#             "question": "When computing the double integral of a function over a rectangular domain, can you choose to integrate with respect to either 'X' or 'Y' first?",
#             "a": [
#                 {
#                     "Yes, when the function is continuous and bounded": [true, "For functions that are continuous and bounded on rectangular domains, the order of integration does not alter the result."]
#                 },
#                 {
#                     "No, the order of integration always affects the result": [false, "For certain types of functions and domains, the order of integration does not influence the result."]
#                 },
#                 {
#                     "Yes, regardless of the nature of the function or domain": [false, "The function being continuous and bounded, and the domain being rectangular, are key conditions."]
#                 },
#                 {
#                     "No, integrals must only be done with respect to 'X' first": [false, "Both orders of integration can be chosen, contingent on the function and domain meeting specific conditions."]
#                 }
#             ]
#         }
#     }
#     """

#     return {"response": json.loads(response)}

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
