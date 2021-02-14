# FSD_capstone
The capstone project for the Udacity full-stack web development nanodegree

The file structure should be like:<br>
![](pics/folder-structure.png)


## Database
A table with the following item:
id

A relational database: 

user id: 
user 

"If the items already exits" 


Questionaire_record:
* ID, 
* question_ID, 
* Right or Wrong. 
* 

**Create Database**
```
psql -U postgres
\l;
CREATE DATABASE databasename;
```

## Authorization
first visit
```
https://hellogaga.eu.auth0.com/authorize?audience=dictionary&response_type=token&client_id=iK5BxRKuFhZfddNMqKxERu9Tjdg95gsL&redirect_uri=http://localhost:5000/
```

it will direct to: Admin
```
http://localhost:5000/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlozRjRBeDlsUWRuYms0ZV9fdDBrMSJ9.eyJpc3MiOiJodHRwczovL2hlbGxvZ2FnYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDYzNDc1Nzg1MjAzNDQyOTMzNDMiLCJhdWQiOlsiZGljdGlvbmFyeSIsImh0dHBzOi8vaGVsbG9nYWdhLmV1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MTMyMzM3NjksImV4cCI6MTYxMzI0MDk2OSwiYXpwIjoiaUs1QnhSS3VGaFpmZGROTXFLeEVSdTlUamRnOTVnc0wiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOnVzZXJzIiwiZGVsZXRlOndvcmRzIiwiZ2V0OmFuc3dlcnMiLCJnZXQ6cXVlc3Rpb25zIiwiZ2V0OnVzZXJzIiwiZ2V0OndvcmRzIiwicGF0Y2g6d29yZHMiLCJwb3N0OmFuc3dlcnMiLCJwb3N0OndvcmRzIl19.Osc6GP6C6YVsWRHD9T0Aj-i1l0wkanwe82qF80u5KWf4pio5zvDp6yLcB2ok1s50g1IVApQisCP0Ao1TosfYkR8Pq8Xdxai5sCysdJuHvA0Yj6FbS2IpbGB-v3Uw2k5ctiCRCHI7oQ1vcp31GIsAasIpnh0-XvrIamzAv1lHWJvhr37jBg68Bh1sppvUXwdqiIl6qyXsAc97f6oo2yZIoI973x8VpKMmm8MtD2JsK-2RBBkKT48fAUwjpQ28NlZRso18fkzjxwkqEBAz4lZJXdBkr2MS6P_Ypl-uu9ZhKk69diEoBAr-T6cO3wysCaNW-JnpsFSqUTqrvt5f5ZufdQ&scope=openid%20profile%20email&expires_in=7200&token_type=Bearer&state=g6Fo2SBCanN1bTFJSWVMWkU4bnkwdlFTUVhvNnVzUXZnRURxSqN0aWTZIHJjd1Jwem81NzFjeEhpRTJFWFJHR2swNUZFb2lBYWdvo2NpZNkgaUs1QnhSS3VGaFpmZGROTXFLeEVSdTlUamRnOTVnc0w
```
A normal user
```
http://localhost:5000/#access_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlozRjRBeDlsUWRuYms0ZV9fdDBrMSJ9.eyJpc3MiOiJodHRwczovL2hlbGxvZ2FnYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZmODkwOWM4ZWZlMDIwMDY4YzBjMWQ1IiwiYXVkIjoiZGljdGlvbmFyeSIsImlhdCI6MTYxMzIzMzc0NiwiZXhwIjoxNjEzMjQwOTQ2LCJhenAiOiJpSzVCeFJLdUZoWmZkZE5NcUt4RVJ1OVRqZGc5NWdzTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOndvcmRzIiwiZ2V0OmFuc3dlcnMiLCJnZXQ6cXVlc3Rpb25zIiwiZ2V0OndvcmRzIiwicGF0Y2g6d29yZHMiLCJwb3N0OmFuc3dlcnMiLCJwb3N0OndvcmRzIl19.XvgsgwqiyhQDXLI4TAYfMDNrQ7lUeJ9WOkP2Nb0jRGG2oJggltP4rlFJYShKWmjVcUFhCQp8EcnlbKGAGyrgCBLcWRaKQay839QrnE28XVGBdUNvRWAnIqUh_pCuIpAOTkyDNihMbHZTkMrkkgHN-C_kqR392ePlZoo95ToywugQ5rS2EKH8dB7J9KETAgkyTNxCpQV8OoZDlEuKzQTAtkfb6qFh5lB7HT0jMSKtpTPTqeiOBBgYvyl01GpctNTOF4qe41hQCTLVFbWoElWi0axhFOH79-fShOuHSRff9LKPfZWQR5Qoj2lYAtiB3MIVCbO7sXCSdej5ype1FUvKuQ&expires_in=7200&token_type=Bearer




```

```
curl --request GET http://localhost:5000/words -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlozRjRBeDlsUWRuYms0ZV9fdDBrMSJ9.eyJpc3MiOiJodHRwczovL2hlbGxvZ2FnYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZmODkwOWM4ZWZlMDIwMDY4YzBjMWQ1IiwiYXVkIjoiZGljdGlvbmFyeSIsImlhdCI6MTYxMjYzNzY5NCwiZXhwIjoxNjEyNjQ0ODk0LCJhenAiOiJpSzVCeFJLdUZoWmZkZE5NcUt4RVJ1OVRqZGc5NWdzTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOndvcmRzIiwiZ2V0OndvcmRzIiwicGF0Y2g6d29yZHMiLCJwb3N0OmFuc3dlcnMiLCJwb3N0OndvcmRzIl19.TcSkMvo_FN6N2MjsK8pFVKbIuq2mmzP4QSKrqRr3XlmprGXfH09bEP-vC4fiQkZW9EawcFVpfXV4ZHSr2_FICRl0d_Ea4DpHwdI09oAsIjP_qVP8qjq5-At3NEjWi4ZnspLNWlnkAxggK3Qu4cXV2ijkAvZ3OWSMjZ9LcR1BCu2gw6_rnNPlP6Fh1Zi3cXF70QpM0BH1392e4wyYK2p9-wEU9cJlBws5aDrueXn3leOxLqZ2Hb9tgIVWmto17q4Wp_bfLDnjyBs2dCjUuizFnVTHjDHUrXzVo4_5ObqKAfxt6ZHDM-IGGjVw-K9fT-he0cMKlZWBFq8f7XA84zaYnA"

```
curl --request DELETE http://localhost:5000/words/6 -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlozRjRBeDlsUWRuYms0ZV9fdDBrMSJ9.eyJpc3MiOiJodHRwczovL2hlbGxvZ2FnYS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWZmODkwOWM4ZWZlMDIwMDY4YzBjMWQ1IiwiYXVkIjoiZGljdGlvbmFyeSIsImlhdCI6MTYxMjYzNzY5NCwiZXhwIjoxNjEyNjQ0ODk0LCJhenAiOiJpSzVCeFJLdUZoWmZkZE5NcUt4RVJ1OVRqZGc5NWdzTCIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOndvcmRzIiwiZ2V0OndvcmRzIiwicGF0Y2g6d29yZHMiLCJwb3N0OmFuc3dlcnMiLCJwb3N0OndvcmRzIl19.TcSkMvo_FN6N2MjsK8pFVKbIuq2mmzP4QSKrqRr3XlmprGXfH09bEP-vC4fiQkZW9EawcFVpfXV4ZHSr2_FICRl0d_Ea4DpHwdI09oAsIjP_qVP8qjq5-At3NEjWi4ZnspLNWlnkAxggK3Qu4cXV2ijkAvZ3OWSMjZ9LcR1BCu2gw6_rnNPlP6Fh1Zi3cXF70QpM0BH1392e4wyYK2p9-wEU9cJlBws5aDrueXn3leOxLqZ2Hb9tgIVWmto17q4Wp_bfLDnjyBs2dCjUuizFnVTHjDHUrXzVo4_5ObqKAfxt6ZHDM-IGGjVw-K9fT-he0cMKlZWBFq8f7XA84zaYnA"
```


admin
{
  "iss": "https://hellogaga.eu.auth0.com/",
  "sub": "google-oauth2|106347578520344293343",
  "aud": [
    "dictionary",
    "https://hellogaga.eu.auth0.com/userinfo"
  ],
  "iat": 1612206779,
  "exp": 1612213979,
  "azp": "iK5BxRKuFhZfddNMqKxERu9Tjdg95gsL",
  "scope": "openid profile email",
  "permissions": [
    "get:words"
  ]
}
yaz@kth.se
{
  "iss": "https://hellogaga.eu.auth0.com/",
  "sub": "auth0|5ff8909c8efe020068c0c1d5",
  "aud": "dictionary",
  "iat": 1612209281,
  "exp": 1612216481,
  "azp": "iK5BxRKuFhZfddNMqKxERu9Tjdg95gsL",
  "scope": "",
  "permissions": []
}

yangzhangkth@gmail.com
{
  "iss": "https://hellogaga.eu.auth0.com/",
  "sub": "google-oauth2|104536530909866680796",
  "aud": [
    "dictionary",
    "https://hellogaga.eu.auth0.com/userinfo"
  ],
  "iat": 1612300428,
  "exp": 1612307628,
  "azp": "iK5BxRKuFhZfddNMqKxERu9Tjdg95gsL",
  "scope": "openid profile email",
  "permissions": [
    "get:words"
  ]
}
```



https://hellogaga.eu.auth0.com/.well-known/jwks.json


## Test
https://stackoverflow.com/questions/48552474/auth0-obtain-access-token-for-unit-tests-in-python/48554119#48554119

https://stackoverflow.com/questions/51192866/flask-rest-api-how-to-use-bearer-api-token-in-python-requests

## This helps understand
https://github.com/gaurangrshah/05-capstone-agency/blob/master/test_api.py


# Docker build
```
docker build --tag dict .
```
Note that the full stop ```.``` tells the docker build command using the Dockerfile found in the current directory.

```
docker run dict -rm
```
where, ```--rm``` option ensures that the container is removed when it exits.

# packages
Flask
Flask-SQLAlchemy
babel
python-dateutil
flask-cors
python-jose
psycopg2
flask_script
flask_migrate
psycopg2-binary