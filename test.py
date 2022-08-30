from src.deep_profane.validator import ProfanityValidator

profane_validator = ProfanityValidator()
res = profane_validator.get_profane_prob(["fuck you"]).tolist()
print(res)

# import requests
# import json

# url = 'http://127.0.0.1:5000/is_profane'
# data = json.dumps({'msg': ["haha"]})

# response = requests.post(url, data=data, headers={"content_type": "application/json"})

# print(response.text)