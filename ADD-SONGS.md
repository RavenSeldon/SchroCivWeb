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

Keep **one** folder holding every track you want, in the order you want them.
This rebuilds `src/assets/audio/` from it each time, so adding, removing and
reordering all work by editing that one folder and re-running.

```bash
brew list ffmpeg >/dev/null 2>&1 || brew install ffmpeg
SOURCE=~/Music/tale-originals          # <-- every track, not just the new ones

# Refuse to run unless SOURCE is set and actually holds files. Without this an
# unset SOURCE expands to /* and ffmpeg walks your whole disk -- after the
# delete below has already emptied the folder.
[ -n "$SOURCE" ] && [ -d "$SOURCE" ] && [ -n "$(ls -A "$SOURCE" 2>/dev/null)" ] || {
  echo "STOP: SOURCE is unset, missing, or empty -- nothing was changed."; return 2>/dev/null || exit 1; }

cd ~/Root/transmission_live/src/assets/audio
find . -maxdepth 1 -name '*.m4a' -delete      # rebuilt from SOURCE below
n=1
for f in "$SOURCE"/*; do
  case "$f" in *.md|*.txt|*/.*) continue;; esac
  name=$(basename "${f%.*}" | tr '[:upper:] ' '[:lower:]_' | tr -cd 'a-z0-9._-')
  ffmpeg -y -loglevel error -i "$f" -vn -c:a aac -b:a 64k -ar 44100 \
         -af "lowpass=f=15000" -movflags +faststart \
         "$(printf '%02d' $n)_${name}.m4a" && n=$((n+1))
done
ls -lh
```

Why it deletes first: the build plays whatever is in this folder, sorted by
filename. Converting only the *new* songs restarts numbering at `01` and
interleaves them with the old ones, and a track removed from `SOURCE` would
otherwise linger here and keep playing. Rebuilding from `SOURCE` every time
makes the folder always match it.

`-y` lets a re-run overwrite silently; without it ffmpeg stops to ask.
`&& n=$((n+1))` means a file that fails to convert doesn't consume a number and
leave a gap in the order.

`-vn` drops any video stream. Music files often carry one — a music video, or
artwork encoded as video — and an `.m4a` container refuses it, so without that
flag ffmpeg writes nothing at all.

**Should say:** five `.m4a` files named `01_…` to `05_…`, a couple of MB each.
They play in that number order, then start again from `01`.

To change the order, renumber the files in `SOURCE` and re-run.

**To slot one track between two existing ones**, give it the number it follows
plus a letter — `04a_…` goes after `04_…` and before `05_…`. Sorting is
locale-aware and ignores `-` and `_`, so `04_04-lament` compares as
`0404lament`: a plain `04_a-good` would sort *before* it, not after. The letter
must ride on the number (`04a_`), not on the title. Renumbering everything
through `SOURCE` is still the cleaner move when you're adding more than one.

**You can also skip this step entirely.** The build accepts any `.mp3`, `.m4a`,
`.aac` or `.ogg` whose name uses only letters, digits, dots, dashes and
underscores — so an already-small, already-tidily-named file can be dropped
straight into `src/assets/audio/`. The conversion exists only to change format,
strip video, shrink the file and clean the name. Note that a `.wav` or `.flac`
dropped in is **ignored without warning**: it isn't an accepted extension, and
the build only warns about accepted extensions with unusable names.

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

**`Could not find tag for codec h264` / `Nothing was written into output file`** —
the source carries a video stream and the `.m4a` container rejects it. Make sure
the ffmpeg line has `-vn` immediately after `-i "$f"`. Check with
`ffprobe -v error -show_entries stream=codec_type -of csv=p=0 yourfile.mp4`; if it
lists `video`, that's the cause.

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
