import requests

import settings

r = requests.get(settings.url)
print(r.html.render)