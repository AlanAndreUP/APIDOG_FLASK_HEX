"""
Endpoints to evaluate:

GET /breeds
GET /breeds/<breed_id>
GET /facts
GET /groups
GET /groups/<group_id>
GET /group-details/<group_id>
GET /group-details/<group_id>/breed/<breed_id>

"""


import urllib.request
import json

total= 0
counter= 0

# Define endpoints to test like this
basic_endpoints = [
    "http://127.0.0.1:5000/breeds",
    "http://127.0.0.1:5000/breeds/68f47c5a-5115-47cd-9849-e45d3c378f12",
    "http://127.0.0.1:5000/facts",
    "http://127.0.0.1:5000/groups",
    "http://127.0.0.1:5000/groups/8000793f-a1ae-4ec4-8d55-ef83f1f644e5"
]

complex_endpoints = [
    "http://127.0.0.1:5000/group-details/8000793f-a1ae-4ec4-8d55-ef83f1f644e5",
    "http://127.0.0.1:5000/group-details/8000793f-a1ae-4ec4-8d55-ef83f1f644e5/breed/68f47c5a-5115-47cd-9849-e45d3c378f12"
]

def eval_resp(task_done= False, fct= 1):
    global total, counter
    
    total+= 1*fct
    if task_done:
        counter+= 1*fct
    return

def test_endpoints(endpoints, title):
    f= 1 if title.lower().startswith("basic") else 2
    print(f"\n{title}")
    for url in endpoints:
        try:
            with urllib.request.urlopen(url) as response:
                status = response.getcode()
                
                is_json= True
                cont= response.read().decode()
                try:
                    json.loads(cont)
                except:
                    is_json= False
                eval_resp(is_json, f)
                
                is_status= status == 200
                if is_status:
                    print(f"200 OK - {url}")
                else:
                    print(f"WRONG {status} - {url}")
                eval_resp(is_status, f)
        except Exception as e:
            print(f"ERROR - {url} - {e}")
            eval_resp(False, f)

if __name__ == "__main__":
    test_endpoints(basic_endpoints, "Basic Endpoints")
    test_endpoints(complex_endpoints, "Complex/Structured Endpoints")
    print(f"\n # Result: {100*counter/total:.1f} %")
