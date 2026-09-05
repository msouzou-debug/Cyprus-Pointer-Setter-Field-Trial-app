/* Κ.Ο.Α.Δ. — offline cache.
   Cache-first for the app shell so the phone works with no signal on the ground.
   Bump CACHE when index.html changes, or the phones keep the old version. */
const CACHE = "koad-v12";
const SHELL = ["./", "./index.html", "./manifest.webmanifest", "./icon.jpg"];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  /* The web fonts are an enhancement, not part of the shell — they are kept
     opportunistically after the first visit so the type survives on the
     terrain, and a miss falls through to the system stack instead of the
     offline page. */
  const font = /fonts\.(googleapis|gstatic)\.com/.test(e.request.url);
  e.respondWith(
    caches.match(e.request).then(hit => hit || fetch(e.request).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(e.request, copy)).catch(() => {});
      return res;
    }).catch(() => font ? Response.error() : caches.match("./index.html")))
  );
});
