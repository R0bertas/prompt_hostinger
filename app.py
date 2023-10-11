from flask import Flask, request, jsonify
import openai
import os

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
    generated_content = {}

    
    print("ROBERTAS")
    for section, section_data  in sections.items():
        
        if section == "about":
            # response = promt_engine("Generate content for the following sections:\n", "About")
            generate_content_about(company_description, section_data, promt_engine)
        
    # Define prompt for OpenAI API
    # prompt = "Generate content for the following sections:\n"
    # for section, section_data in sections.items():
    #     if 'title' in section_data:
    #         prompt += f"**{section_data['title']}**\n"
    #     if 'subtitle' in section_data:
    #         prompt += f"*{section_data['subtitle']}*\n"
    #     if 'description' in section_data:
    #         for _ in range(section_data['description']):
    #             prompt += "Generate a paragraph related to this section.\n"
    #     prompt += "\n"

    # # Call OpenAI API to generate text
    # response = openai.ChatCompletion.create(
    #             model="gpt-3.5-turbo",
    #             messages=[
    #                 {"role": "system", "content": "You must provide answer in the same language as the question."},
    #                 {"role": "user", "content": prompt},
    #             ],
    #             temperature=0.5, 
    #             max_tokens=20,
    #         )

 

    # generated_text = response.choices[0].message['content']

    # # Organize the generated content
    # for section in sections:
    #     generated_content[section] = {'description': generated_text}

    # return jsonify(generated_content), 200
    return jsonify(generated_content), 200


def generate_content_about(company_description, data, response_from_openai):
    
    # we will build structure for about section
    about_section = {}

    # getting number of titles, subtitles and descriptions
    #  if it is not provided set it to 0 and if it is 1 it will be string otherwise list 
    number_of_titles =data.get("title", 0)
    number_of_subtitles =data.get("subtitle", 0)
    number_of_descriptions =data.get("description", 0)

    if number_of_titles == 1:
        about_section.update({"title": response_from_openai("Generate title based on user description for the about section:\n", f"Here is a company description {company_description} write a title for it")})
    if number_of_titles > 1:
        number_of_responses = []
        for _ in range(number_of_titles+1):
            number_of_responses.append(response_from_openai("Generate title based on user description for the about section:\n", f"Here is a company description {company_description} write a title for it"))
        about_section.update({"title": number_of_responses} )   
        
    if number_of_subtitles == 1:
        about_section.update({"subtitle": response_from_openai("Generate subtitle based on user description for the about section:\n", f"Here is a company description {company_description} write a subtitle for it")})
    if number_of_subtitles > 1:
        number_of_responses = []
        for _ in range(number_of_titles+1):
            number_of_responses.append(response_from_openai("Generate subtitle based on user description for the about section:\n", f"Here is a company description {company_description} write a subtitle for it"))
        about_section.update({"subtitle": number_of_responses}   )
    
    if number_of_descriptions == 1:
        about_section.update({"description": response_from_openai("Generate subtitle based on user description for the about section:\n", f"Here is a company description {company_description} write a description for it")})
    if number_of_descriptions > 1:
        number_of_responses = []
        for x in range(number_of_titles+1):
            number_of_responses.append(response_from_openai("Generate subtitle based on user description for the about section:\n", f"Here is a company description {company_description} write a description for it"))
        about_section.update({"description": number_of_responses} )    
        
    print("EEEEEEEEE", about_section)
    return about_section

def generate_content_refunds():
    pass

def generate_content_hero():
    pass

def promt_engine(system_prompt,user_prompt):
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.5, 
                max_tokens=20,
            )
    
    return response.choices[0].message['content']

if __name__ == "__main__":
    app.run(debug=True)
