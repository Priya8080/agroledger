import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = {
    "static/js/tailwind.js": "https://cdn.tailwindcss.com",
    "static/js/alpine.min.js": "https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"
}

for path, url in urls.items():
    print(f"Downloading {url} to {path}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx) as response, open(path, 'wb') as out_file:
            data = response.read()
            out_file.write(data)
        print(f"Success: {path}")
    except Exception as e:
        print(f"Failed: {path} - {e}")
