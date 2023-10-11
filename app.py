from flask import Flask, request, jsonify
import openai
import os
# to keep the order of the keys in the dictionary as in response from task 
from collections import OrderedDict
# from concurrent.futures import ThreadPoolExecutor

app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

@app.route("/rephrase", methods=["POST"])
def rephrase_text():
    
    auth = request.authorization
    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        return jsonify({'message': 'Authentication failed'}), 401
    try:
        data = request.json
        text_to_rephrase = data["text"]
        # making if person does not enter set number of variants as default 2
        number_of_variants = data.get("number_of_variants", 2)

        rephrased_variants = []
        
        prompt=f"Rephrase the following text and keep in the same language it was provided: {text_to_rephrase}"

        for _ in range(number_of_variants):

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You must provide answer in the same language as the question."},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5, 
                max_tokens=20,
            )
            rephrased_variants.append(response.choices[0].message['content'])
            

        return jsonify(rephrased_variants)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/generate-content', methods=['POST'])
def generate_section_content():
    # Basic Authentication
    auth = request.authorization
    if not auth or auth.username != USERNAME or auth.password != PASSWORD:
        return jsonify({'message': 'Authentication failed'}), 401

    # Parse the request data
    data = request.get_json()

    # Check if 'sections' field is present in the request
    if 'sections' not in data or "description" not in data:
        return jsonify({'message': 'Missing "sections" or "description" field in the request'}), 400

    sections = data['sections']
    company_description = data['description']

    # Generate content for each section
    generated_content =  OrderedDict()

    
    for section, section_data  in sections.items():
        # the reason i went with if statements is because we may want to have different prompts for each section
        #  more flexibility to modify sections if content about will have something what others may not need 
        #  we could generalize these 3 functions into one but i think it is better to have them separate
        if section == "about":
            about_resp = generate_content_about(company_description, section_data, prompt_engine)
            generated_content["about"] = about_resp
        if section == "refunds":
            refunds_resp = generate_content_refunds(company_description, section_data, prompt_engine)
            generated_content["refunds" ] = refunds_resp
        if section == "hero":
            hero_resp = generate_content_hero(company_description, section_data, prompt_engine)
            generated_content["hero"] = hero_resp
                                      

  
    return jsonify(generated_content), 200


def generate_content_about(company_description, data, response_from_openai):
    
    # we will build structure for about section
    about_section = OrderedDict()
    
    for key in ["title", "subtitle", "description"]:
        system_prompt = f"Generate {key} based on user description for the about section"
        user_prompt = f"Here is a company description {company_description} write a {key} for it"
        
        num_items = data.get(key, 0)
        if num_items == 1:
            about_section[key] = response_from_openai(system_prompt, user_prompt)
        elif num_items > 1:
            number_of_responses = []
            for _ in range(num_items):
                number_of_responses.append(response_from_openai(system_prompt, user_prompt))
            about_section[key] = number_of_responses

    return about_section

def generate_content_refunds(company_description, data, response_from_openai):
        
    refunds_section = OrderedDict()

    for key in ["title", "subtitle", "description"]:
        
        system_prompt = f"Generate {key} based on user description for the refunds section"
        user_prompt = f"Here is a company description {company_description} write a {key} for it, mention refunds" 
        
        num_items = data.get(key, 0)
        if num_items == 1:
            refunds_section[key] = response_from_openai(system_prompt, user_prompt)
        elif num_items > 1:
            number_of_responses = []
            for _ in range(num_items):
                number_of_responses.append(response_from_openai(system_prompt, user_prompt))
            refunds_section[key] = number_of_responses
    
    
    return refunds_section
# code same as generate_content_about
def generate_content_hero(company_description, data, response_from_openai):
    
    hero_section = OrderedDict()
    
    for key in ["title", "subtitle", "description"]:
    
        system_prompt = f"Generate {key} based on user description for the hero section"
        user_prompt = f"Here is a company description {company_description} write a {key} for it, hero section means somethin unique "
        
        num_items = data.get(key, 0)
        if num_items == 1:
            hero_section[key] = response_from_openai(system_prompt, user_prompt)
        elif num_items > 1:
            number_of_responses = []
            for _ in range(num_items):
                number_of_responses.append(response_from_openai(system_prompt, user_prompt))
            hero_section[key] = number_of_responses

    
        return hero_section
    
    

def prompt_engine(system_prompt,user_prompt):
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.8, 
                max_tokens=50,
            )
    
    return response.choices[0].message['content']
    return "test"

if __name__ == "__main__":
    app.run(debug=True)
