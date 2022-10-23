from google.oauth2 import id_token
from google.auth.transport import requests

# (Receive token by HTTPS POST)
# ...

idinfo = id_token.verify_oauth2_token(
    'eyJhbGciOiJSUzI1NiIsImtpZCI6ImVlMWI5Zjg4Y2ZlMzE1MWRkZDI4NGE2MWJmOGNlY2Y2NTliMTMwY2YiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiI0MzI0MjEyOTU4OTQtMXNvcTI2MjVjN21zY3FrcHJxZG1xaGRrNDNldDI4anUuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiI0MzI0MjEyOTU4OTQtc3NhNG0wMGYwYXEzNW5tNjZ0amFnNTY0MmFvMmxoOGcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTY2MTAyNzkwODM3NDQzMDE3MTEiLCJlbWFpbCI6InRyYW5kdWNkdXk3NTIwQGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJuYW1lIjoiRHV5IFRy4bqnbiIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BTG01d3UzVm5aYzZBSEFuTm9UbFpWcDR1amxvZmRHODY5c3BHZFZOc0xlMDNnPXM5Ni1jIiwiZ2l2ZW5fbmFtZSI6IkR1eSIsImZhbWlseV9uYW1lIjoiVHLhuqduIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2NjY1MzE0MjEsImV4cCI6MTY2NjUzNTAyMX0.Woj58KVzBILvjouqOsjLj1IjZVDXaV8rpcdCeTonSv5S8HPaoiq3BqnPLOf0GXggRV3FeOoKCHEM43P-HTorurtpVHS8jz9L3RRrynX-YJMNIx5Mud7Kiie2rBuZPmx_1qE1D62h0N3rhYRPcrakU_TvaeFgMPxKFgt1EcP-_VSnuijz20P7CMuf0ccEs5p99LBve82J2PloNmdRmlbfTejUDvKqybBY5VdaUD_-91aYU9ULsYgTDBqvUR4RXU5bj_1FOVDKeN9oEu0z92O4AG3uuOlOp2CuXyqb80reAnQC6A25_k7iRla1mJ3XZdFfXM7ct0oE7TVNbHAHNk0LKw', requests.Request(), '432421295894-ssa4m00f0aq35nm66tjag5642ao2lh8g.apps.googleusercontent.com')

# Or, if multiple clients access the backend server:
# idinfo = id_token.verify_oauth2_token(token, requests.Request())
# if idinfo['aud'] not in [CLIENT_ID_1, CLIENT_ID_2, CLIENT_ID_3]:
#     raise ValueError('Could not verify audience.')

# If auth request is from a G Suite domain:
# if idinfo['hd'] != GSUITE_DOMAIN_NAME:
#     raise ValueError('Wrong hosted domain.')

# ID token is valid. Get the user's Google Account ID from the decoded token.
userid = idinfo['sub']

print(idinfo)
