# Adding songs to the Tale — do these in order

Everything here runs on **your Mac**, in Terminal. Copy one block at a time.
After each block, check the "should say" line before moving on.

---

## STEP 0a — one time only: the `neurascape` shortcut

Every deploy command below says `neurascape`. That is a nickname for your
droplet, defined once on your Mac. Check it exists:

```bash
ssh neurascape 'whoami'
```

**If it prints a username**, you're set. Skip to Step 0b.

**If it says `Could not resolve hostname`**, create it. Use whichever of `root`
or `myuser` answers `ssh -i ~/.ssh/neurascape_key USER@159.203.34.8 'whoami'`;
prefer `root` if both do, so `sudo` never prompts you during a deploy:

```bash
cat >> ~/.ssh/config <<'EOF'

Host neurascape
    HostName 159.203.34.8
    User root
    IdentityFile ~/.ssh/neurascape_key
EOF
chmod 600 ~/.ssh/config
ssh neurascape 'whoami'
```

---

## STEP 0b — one time only, skip if already done

Audio will not play until the blog knows what an audio file is.

```bash
cd ~/PycharmProjects/PythonProject/WebDev/Blog
git status --short
```

**If nothing prints**, it's already done. Skip to Step 1.

**If it lists `app/routes/schrodingers_civ/views.py`**, run:

```bash
git add app/routes/schrodingers_civ/views.py
git commit -m "Serve audio MIME types from the publication blueprint"
git push
ssh -t neurascape 'cd /var/www/Neurascape/WebDev/Blog && git pull && sudo systemctl kill -s HUP blog.service'
```

---

## STEP 1 — convert your songs

Put your original files in one folder, then set `SOURCE` to it:

```bash
brew list ffmpeg >/dev/null 2>&1 || brew install ffmpeg
SOURCE=~/Music/tale-originals          # <-- change this to your folder

cd ~/Root/transmission_live/src/assets/audio
n=1
for f in "$SOURCE"/*; do
  name=$(basename "${f%.*}" | tr '[:upper:] ' '[:lower:]_' | tr -cd 'a-z0-9._-')
  ffmpeg -loglevel error -i "$f" -c:a aac -b:a 64k -ar 44100 \
         -af "lowpass=f=15000" -movflags +faststart \
         "$(printf '%02d' $n)_${name}.m4a"
  n=$((n+1))
done
ls -lh
```

**Should say:** five `.m4a` files named `01_…` to `05_…`, a couple of MB each.
They play in that number order, then start again from `01`.

To change the order, rename the number prefixes.

---

## STEP 2 — build and listen

```bash
cd ~/Root/transmission_live
node scripts/build.mjs
npm run check
npm run preview
```

**Should say:** `Built 31 static routes…` then `All local links … passed.`

`npm run preview` gives you a local address. Open it, click **The Translator's
Tale**, open a chapter, and press the star in the bottom-right corner.

Listen at your normal volume for a minute. Too loud or too quiet? Open
`src/app.js`, find `taleEl.volume=0.4`, change the number (0.25 is quieter,
0.6 louder), then run `node scripts/build.mjs` again and re-listen.

Press Ctrl+C in Terminal to stop the preview.

---

## STEP 3 — save it

```bash
cd ~/Root/transmission_live
find .git -name '*.lock' -delete
git add -A src/assets/audio
git status --short
```

**Should say:** your five `.m4a` files, nothing else unexpected.

```bash
git commit -m "Add the Tale soundtrack"
git push
```

This saves your work to GitHub. **It does not put it on the website yet.**

---

## STEP 4 — put it on the website

```bash
cd ~/Root/transmission_live
REL=$(date +%Y%m%d-%H%M%S)
echo "REL=$REL"
ssh neurascape "mkdir -p ~/scw-staging/${REL}"
rsync -a --delete dist/ "neurascape:scw-staging/${REL}/"
```

**Should say:** no errors. The upload takes a few seconds per song.

Then, in the **same Terminal window**:

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

**Should say:** `installing: <your REL>` then `current -> …/releases/<your REL>`.
It will ask for your droplet password once.

No restart needed. This is static content behind a symlink.

---

## STEP 5 — check it worked

```bash
curl -sI https://www.benamuwo.me/schrodingers_civ/assets/audio/01_*.m4a | head -3
```

**Should say:** `HTTP/2 200` **and** `content-type: audio/mp4`.

Then open a chapter on the real site, press the star, and click through to the
next chapter. The music should carry on rather than start over.

---

## If something goes wrong

**Star appears but nothing plays** — Step 0 wasn't done, or hasn't reached the
droplet. Check with the `curl` in Step 5: if it says `application/octet-stream`
instead of `audio/mp4`, that's it.

**No star at all** — the files aren't in `src/assets/audio/`, or you deployed
before building. Run `ls ~/Root/transmission_live/src/assets/audio/`, then redo
Steps 2 and 4.

**`zsh: no matches found`** — a `*` matched nothing and zsh gave up on the whole
line. Nothing ran. Not your fault; re-run with a real filename.

**`Unable to create '.git/index.lock'`** — run `find .git -name '*.lock' -delete`
and try again.

**Music restarts every chapter instead of continuing** — expected in a private /
incognito window, where the browser blocks the storage that remembers the
position. Normal windows are fine.

**Undo the whole thing** — put the site back to the previous release:

```bash
ssh neurascape 'ls -1 /srv/schrodingers-civ/releases/'
ssh -t neurascape 'sudo ln -sfn /srv/schrodingers-civ/releases/<PICK-THE-ONE-BEFORE> /srv/schrodingers-civ/current.new && sudo mv -T /srv/schrodingers-civ/current.new /srv/schrodingers-civ/current'
```

To remove the music but keep everything else: delete the `.m4a` files from
`src/assets/audio/`, then do Steps 2, 3 and 4. With the folder empty the star
disappears completely.
