# Deploying benamuwo.me

Two separate sites live on one droplet. They deploy differently and must not be
confused.

| | Schrödinger's Civilization | Neurascape (the blog) |
|---|---|---|
| What it is | Static HTML built from this repo | Flask app |
| Repo | `SchroCivWeb` → `~/Root/transmission_live` | `~/PycharmProjects/PythonProject/WebDev/Blog` |
| Lives on droplet at | `/srv/schrodingers-civ/current/` | `/var/www/Neurascape/WebDev/Blog` |
| Deploy = | rsync files, swap a symlink | `git pull` + reload workers |
| Needs a service restart? | **No** | **Yes** (`blog.service`) |
| URL | `/schrodingers_civ/` | everything else |

**Two machines.** Everything with `node`, `npm`, `git` or `python3` in it runs on
your **Mac**. The droplet only ever receives files. If a command block starts by
`cd`-ing somewhere in your Mac's filesystem, it runs on the Mac — including the
`ssh` and `rsync` lines, which reach *out* to the droplet from there.

**Never touch `gunicorn.service`.** That's a different Django project. The blog
is `blog.service`.

---

## Setup (once)

Add to `~/.ssh/config` so you never type `-i` or an IP again:

```
Host neurascape
    HostName 159.203.34.8
    User root
    IdentityFile ~/.ssh/neurascape_key
```

Check Node is 22+ (`node -v`). If not: `brew install node && hash -r`.

---

## A. Changing Schrödinger's Civilization

Anything under `/schrodingers_civ/` — pages, papers, artwork, styles, the banner.

### 1. Make the change

Edit files in `~/Root/transmission_live/src/` or `scripts/build.mjs`.
**Never edit `dist/`** — it is regenerated from scratch on every build and your
edit would vanish.

### 2. Build and look at it

```bash
cd ~/Root/transmission_live
node scripts/build.mjs
npm run preview        # opens a local server; check the pages you changed
```

Expect: `Built 31 static routes at /schrodingers_civ/; NN ... assets.`
If the build errors, stop. Do not deploy a failed build — `dist/` will be stale
or half-written, and you will ship the previous version without noticing.

### 3. Commit

```bash
git status --short     # confirm only the files you meant to change
git add -A
git commit -m "Short description of what changed"
git push
```

`dist/` will not appear — it is gitignored on purpose. The repo stores sources;
the droplet gets the built output in the next step.

### 4. Push it live

```bash
cd ~/Root/transmission_live
REL=$(date +%Y%m%d-%H%M%S)
ssh neurascape "mkdir -p ~/scw-staging/${REL}"
rsync -a --delete dist/ "neurascape:scw-staging/${REL}/"
```

```bash
ssh neurascape 'cat > ~/scw-install.sh' <<'EOF'
set -e
HOMEDIR=$(getent passwd "${SUDO_USER:-$USER}" | cut -d: -f6)
REL=$(ls -1 "$HOMEDIR/scw-staging" | sort | tail -1)
echo "installing: $REL"
test -f "$HOMEDIR/scw-staging/$REL/index.html" || { echo "ABORT: no index.html"; exit 1; }
mkdir -p "/srv/schrodingers-civ/releases/$REL"
rsync -a --delete "$HOMEDIR/scw-staging/$REL/" "/srv/schrodingers-civ/releases/$REL/schrodingers_civ/"
chown -R root:root "/srv/schrodingers-civ/releases/$REL"
chmod -R a+rX "/srv/schrodingers-civ/releases/$REL"
ln -sfn "/srv/schrodingers-civ/releases/$REL" /srv/schrodingers-civ/current.new
mv -T /srv/schrodingers-civ/current.new /srv/schrodingers-civ/current
echo "current -> $(readlink -f /srv/schrodingers-civ/current)"
EOF

ssh -t neurascape 'sudo bash ~/scw-install.sh'
```

The symlink swap is atomic: visitors see the old release or the new one, never a
half-copied directory. **No restart is needed** — the Flask view resolves the
`current` symlink on every request.

### 5. Check

```bash
curl -sI https://www.benamuwo.me/schrodingers_civ/ | head -1     # 200
curl -sI https://www.benamuwo.me/ | head -1                      # 200 -- blog still fine
```

Then hard-refresh the page (Cmd+Shift+R).

### Rollback

```bash
ssh neurascape 'ls -1 /srv/schrodingers-civ/releases/'    # pick the previous timestamp
ssh -t neurascape 'sudo ln -sfn /srv/schrodingers-civ/releases/<PREVIOUS> /srv/schrodingers-civ/current.new && sudo mv -T /srv/schrodingers-civ/current.new /srv/schrodingers-civ/current'
```

Instant, and no restart.

---

## B. Changing the Neurascape blog

Templates, routes, styles — anything outside `/schrodingers_civ/`.

### 1. Make the change

Edit in `~/PycharmProjects/PythonProject/WebDev/Blog`.

### 2. Test locally

```bash
cd ~/PycharmProjects/PythonProject/WebDev/Blog
flask run      # visit the pages you changed, plus the homepage
```

### 3. Commit

```bash
git status --short
git add <the specific files>
git commit -m "Short description"
git push
```

### 4. Push it live

```bash
ssh -t neurascape
cd /var/www/Neurascape/WebDev/Blog && git pull
sudo systemctl kill -s HUP blog.service      # graceful; no dropped requests
exit
```

`systemctl reload` does **not** work on this unit — it defines no `ExecReload`.
`kill -s HUP` recycles the gunicorn workers gracefully. `systemctl restart`
also works but drops requests for a second or two.

### 5. Check

```bash
curl -sI https://www.benamuwo.me/ | head -1                      # 200
curl -sI https://www.benamuwo.me/schrodingers_civ/ | head -1     # 200 -- publication still fine
```

---

## If something looks wrong

| Symptom | Meaning |
|---|---|
| `/schrodingers_civ/` gives **503** | Blueprint is running, files are missing. Check `/srv/schrodingers-civ/current/schrodingers_civ/index.html` exists and is world-readable. |
| `/schrodingers_civ/` gives **404** | Files are fine, the Flask blueprint is not loaded. Blog side: did the `git pull` and HUP happen? |
| Change deployed but page looks old | Browser cache. Hard-refresh. If `curl` also shows the old content, the symlink never moved — re-run step 4. |
| `bad substitution` in zsh | Brace the variable: `"${HOST}:path"`, not `"$HOST:path"`. |
| `Identity file not accessible` / `Could not resolve hostname` (blank) | Shell variables are empty — new terminal tab. Re-set them, or use the `~/.ssh/config` alias. |
| `sudo: a terminal is required` | You fed a script to `ssh` on stdin. Use `ssh -t ... 'sudo bash ~/script.sh'` instead. |
| `Unexpected token '.'` from node | Old Node on PATH. `node -v` must be 22+. |
| git: `Unable to create '.git/index.lock'` | A stale lock. `rm -f .git/*.lock .git/objects/*.lock`, then retry. |

---

## Two rules worth keeping

**Never edit `dist/`.** It is deleted and rebuilt every time.

**Endpoint names in the Flask blog must not collide.** `create_app()` aliases
`blueprint.name` down to a bare `name`. An endpoint called `index` anywhere
would steal `url_for('index')` from the homepage and break the nav link on every
page. This is why the publication's endpoints are prefixed `schrociv_`.
