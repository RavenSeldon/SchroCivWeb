# Tale soundtrack

Drop `.mp3`, `.m4a`, `.aac` or `.ogg` files here. The next build picks them up
automatically: a star toggle appears on the 23 chapter pages, the tracks play in
filename order, and playback position carries across chapter turns.

Empty folder = no player is emitted at all. Nothing else to configure.

Name files with letters, digits, dots, dashes and underscores only — no spaces.
The build skips anything else and says so, because a space in a filename produces
a URL that `npm run check` cannot resolve.

One file loops gaplessly. Several play as a playlist and wrap around at the end.
Volume defaults to 40%; change `taleEl.volume` in `src/app.js`.
