"""Test only the supplied blueprint in a new Flask app; never import the blog."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from flask import Flask

root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'docs/flask-integration'))
from schrodingers_civ.url import schrodingers_civ_bp
os.environ['SCHRODINGERS_CIV_ROOT'] = str(root / 'dist')
app = Flask('isolated_publication_test', static_folder=None)
app.register_blueprint(schrodingers_civ_bp)
@app.get('/')
def existing_home():
    return 'Existing root route'
client = app.test_client()
checks = []
for route in json.loads((root / 'dist/routes.json').read_text()):
    url = '/schrodingers_civ/' + route['route']
    response = client.get(url)
    assert response.status_code == 200, (url, response.status_code)
    assert response.data == (root / 'dist' / route['route'] / 'index.html').read_bytes()
    assert client.head(url).status_code == 200
    checks.append(url)
assert client.get('/').data == b'Existing root route'
for suffix in ['', '/atlas', '/tale/epilogue']:
    response = client.get('/schrodingers_civ' + suffix + '?q=hello%20world')
    assert response.status_code == 308
    assert response.headers['Location'].endswith(suffix + '/?q=hello%20world')
for url in ['/schrodingers_civ/missing/', '/schrodingers_civ/../README.md', '/schrodingers_civ/%2e%2e/README.md']:
    response = client.get(url)
    assert response.status_code == 404, url
    assert response.data == (root / 'dist/404.html').read_bytes()
for asset in json.loads((root / 'dist/assets/source-manifest.json').read_text())['assets']:
    response = client.get('/schrodingers_civ/' + asset['path'])
    assert response.status_code == 200
    assert hashlib.sha256(response.data).hexdigest() == asset['sha256']
    assert response.headers['Cache-Control'] == 'no-cache'
# Check both hostname spellings without changing global host routing.
for host in ['benamuwo.me', 'www.benamuwo.me']:
    assert client.get('/schrodingers_civ/', base_url='https://' + host).status_code == 200
with tempfile.TemporaryDirectory(dir=root / 'qa') as directory:
    sandbox = Path(directory)
    public = sandbox / 'public'; public.mkdir()
    private = sandbox / 'private.txt'; private.write_text('not public')
    (public / 'escape.txt').symlink_to(private)
    os.environ['SCHRODINGERS_CIV_ROOT'] = str(public)
    assert client.get('/schrodingers_civ/escape.txt').status_code == 404
    os.environ['SCHRODINGERS_CIV_ROOT'] = str(sandbox / 'not-installed')
    assert client.get('/schrodingers_civ/').status_code == 503
report = {'result': 'PASS', 'htmlRoutes': len(checks), 'assetHashes': 46,
          'checks': ['GET and HEAD routes', 'exact static bytes', 'root route unaffected',
                     'trailing slash and query preservation', 'publication 404',
                     'path traversal and symlink escape rejected', 'both hostnames',
                     'missing installation 503'],
          'isolation': 'Fresh Flask app with only the supplied blueprint; no blog import, database, model or migration access.'}
(root / 'qa/flask-wiring-check.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2))
