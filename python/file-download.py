import requests

url = ''
r = requests.get(url, allow_redirects=True)
open('filename.ext', 'wb').write(r.content)