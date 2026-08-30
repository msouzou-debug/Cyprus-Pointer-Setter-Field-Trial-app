# Κ.Ο.Α.Δ. Trial Manager — putting it on the laptop and the phones

## Why it needs a web address

The app is one HTML file and it runs with no server. But **Safari on the iPhone refuses to save anything when a page is opened straight from a file.** Email yourself the file, tap it in Files, and everything you type is gone the moment you close the tab. The app now detects this and shows a red bar saying so, but the fix is to put it at a web address.

Once it has one, both the laptop and the phones open the same link, install it to the home screen, and it works with no signal on the ground.

Hosting is free and there is no server to maintain. Pick one.

## Option 1 — Cloudflare Pages (recommended, 5 minutes, no account juggling)

1. Go to `pages.cloudflare.com` and sign up. Free.
2. **Create a project → Upload assets.**
3. Drag in these four files: `index.html`, `manifest.webmanifest`, `sw.js`, `icon.jpg`.
4. Name it, e.g. `koad-agones`. It publishes at `https://koad-agones.pages.dev`.
5. Open that address on the laptop and on every phone that needs it.

## Option 2 — Netlify Drop (fastest, no account needed to try)

1. Go to `app.netlify.com/drop`.
2. Drag the folder containing the four files onto the page.
3. It gives you an address immediately. Claim it with a free account to keep it.

## Option 3 — GitHub Pages

Put the four files in a repository, then Settings → Pages → deploy from the `main` branch, root folder.

---

## Installing on the phone

**iPhone / iPad (Safari — it must be Safari, not Chrome)**
Open the address → Share button → **Πρόσθεση στην Οθόνη Αφετηρίας** / Add to Home Screen → Add.

**Android (Chrome)**
Open the address → menu (⋮) → **Εγκατάσταση εφαρμογής** / Install app.

Either way you get an icon with the club badge, no browser bars, and the app opens straight into the trial. After the first visit it works with no signal, which is what matters on the terrain.

## Installing on the laptop

Open the address in Chrome or Edge and use the install icon in the address bar. Or just bookmark it — a laptop is rarely out of signal.

---

## Important: each device keeps its own data

There is no server, so nothing syncs by itself. The laptop and the phone each have their own copy.

The working pattern:

1. **Laptop, before the trial** — import the dog registry, add the entries, set up the terrains and judges.
2. **Ρυθμίσεις → Μεταφορά → Αποστολή πλήρους αντιγράφου.** Send the file to the phone by WhatsApp, Viber, Messenger or email.
3. **Phone** — save the file, then **Φόρτωση αρχείου → Συγχώνευση**.
4. **On the ground** — draw, send the SMS, record the notes and results.
5. **After** — send the file back from the phone the same way and merge it on the laptop.

Merge keeps whatever is already on the device and adds or updates the rest, so nothing you did on the laptop in the meantime is lost.

**One rule:** move in one direction at a time. If you edit the same trial on both devices between transfers, the file loaded last wins for that trial.

## Updating the app

Replace `index.html` at the host, then **change `CACHE = "koad-v1"` to `"koad-v2"` in `sw.js`** and upload that too. Without the version bump the installed phones keep serving the old copy from cache.

Data survives an update — it is stored separately from the app.

## Backups

Ρυθμίσεις → Μεταφορά → **Λήψη στη συσκευή**, after every trial. Keep the file. Clearing the browser's site data on that phone erases everything otherwise.
