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

docker run -e OPENAI_API_KEY=your_key -p 5000:5000 your-app-name

```
if you get error
docker: Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:5000 -> 0.0.0.0:0: listen tcp 0.0.0.0:5000: bind: address already in use.
ERRO[0000] error waiting for container

modify docker file to use different port etc 5001


Future update suggestions:

0. Use oauth for authentication
1. Add more test cases
2. Add pydantic for validation
3. Add limitation for number_of_variants
4. Provide limitation on a response size


<!-- Comands for testing 2 endpoints -->
 curl -u your_username:your_password -X POST -H "Content-Type: application/json" -d '{"text": "Original text goes here.", "number_of_variants": 2}' http://localhost:5000/rephrase


curl  -u your_username:your_password -X POST -H "Content-Type: application/json" -d '{ "description": "User business description", "sections": { "about": { "title": 1, "description": 2 }, "refunds": { "title": 1, "description": 1 }, "hero": { "title": 1, "subtitle": 1 } } }' http://localhost:5000/generate-content

<!--
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