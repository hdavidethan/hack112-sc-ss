import urllib.request

images = {}
images["something"] = "url"

for key in images:
    url = images["key"]
    ext = url[url.rfind("."):]
    urllib.request.urlretrieve(url, key+ext)