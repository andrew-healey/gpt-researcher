import urllib.request
import json

def visit(url,as_markdown=False):
    base_url = 'http://localhost:9999/page'
    mode = 'markdown' if as_markdown else 'noNavigation'
    params = {
        'url': url,
        'mode': mode
    }
    full_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(full_url) as response:
            resp = response.read().decode('utf-8')
            parsed_json = json.loads(resp)
            return parsed_json["text"],parsed_json["html"]
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")

    return None