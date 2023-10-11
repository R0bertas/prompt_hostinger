----How to execute without docker

open terminal and run the following commands

```bash
python app.py
```

open another terminal and run the following commands

```bash
 curl -u your_username:your_password -X POST -H "Content-Type: application/json" -d '{"text": "Original text goes here.", "number_of_variants": 2}' http://localhost:5000/rephrase
 ```



----Docker

open terminal and run the following commands

```bash
docker build -t your-app-name .

docker run -p 5000:5000 your-app-name
```



Future update suggestions:
0. Use oauth for authentication
1. Add more test cases
2. Add pydantic for validation
3. Add limitation for number_of_variants
4. Provide limitation on a response size


<!-- Comands for testing 2 endpoints -->
 curl -u your_username:your_password -X POST -H "Content-Type: application/json" -d '{"text": "Original text goes here.", "number_of_variants": 2}' http://localhost:5000/rephrase




<!-- 
curl  -u your_username:your_password -X POST -H "Content-Type: application/json" -d '{ "description": "User business description", "sections": { "about": { "title": 1, "description": 2 }, "refunds": { "title": 1, "description": 1 }, "hero": { "title": 1, "subtitle": 1 } } }' http://localhost:5000/generate-content


Request body Based on description 
{
    "description": "User business description",
    "sections": {
        "about": {
            "title": 1,
            "subtitle": 1,
            "description": 2
        },
        "refunds": {
            "title": 1,
            "subtitle": 1,
            "description": 1
        },
        "hero": {
            "title": 1,
            "subtitle": 1,
            "description": 1
        }
    }
} 
-->
<!--  
Response body
{
    "about": {
        "title": "Apie mus",
        "description": [
            "Mes kuriamame unikalius produktus naudodami kvarcinį smėlį. Kvarcas yra inovatyvi ",
            "Sukuriame unikalius produktus, pasitelkdami kvarcinį smėlį, kuris yra inovatyvi i"
        ],
        "refunds": {
            "title": "Informacija apie grąžinimus",
            "description": "Sužinokite daugiau apie mūsų grąžinimo politiką ir kaip gauti pinigus"
        },
        "hero": {
            "title": "Unikalus produktų kūrimas",
            "subtitle": "Kvarcinio smėlio naudojimas"
        }
    }
} 
-->

You are working as an Al developer at a amazing company. Your colleague from the Website Builder team approaches you with a need to have a few new Al features in Website Builder:
1. Allows users to automatically generate content for specific website sections based on user-provided business description.

Section content generation feature
The input for this feature consists of user-provided business descriptions and a section structure needed for a website. The output is the provided structure enhanced with generated text.
You agreed that the section content generation endpoint will accept such HTTP request:
{
    "description": "User business description",
    "sections": {
        "about": {
            "title": 1,
            "description": 2
        },
        "refunds": {
            "title": 1,
            "description": 1
        },
        "hero": {
            "title": 1,
            "subtitle": 1
        }
    }
} 
Where the sections object contains information about what sections are needed for the user's website, and each section can have title, subtitle, and description (they are all optional) fields that describe the section. For example about section can have title and description fields required in one request/case, but title, subtitle, and description on the next request/case. Each section fields are optional. You agreed that for now only about, refunds and hero sections will be supported by your API. Keep in mind that some websites might not use all of the sections, for example, only about and hero sections are needed.

Response from your API endpoint would look like this:
{
    "about": {
        "title": "Apie mus",
        "description": [
            "Mes kuriamame unikalius produktus naudodami kvarcinį smėlį. Kvarcas yra inovatyvi ",
            "Sukuriame unikalius produktus, pasitelkdami kvarcinį smėlį, kuris yra inovatyvi i"
        ],
        "refunds": {
            "title": "Informacija apie grąžinimus",
            "description": "Sužinokite daugiau apie mūsų grąžinimo politiką ir kaip gauti pinigus"
        },
        "hero": {
            "title": "Unikalus produktų kūrimas",
            "subtitle": "Kvarcinio smėlio naudojimas"
        }
    }
} 
The tasks for you and constraints:
1. Create RESTful API with one endpoint:  for section content generation.
2. Use Python programming language.
3. Implement authentication for your API endpoints (basic auth or bearer token is good enough).
4. Your API should be robust so think about error handling.
5. Use OpenAI API for text generation.
5.1. Perform prompt engineering to achieve the results.# prompt_hostinger
