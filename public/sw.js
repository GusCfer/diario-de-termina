// Cache para funcionar offline. A página usa "rede primeiro" para sempre pegar a versão nova quando houver internet.
const CACHE = "termina-v16";
const CORE = ["./", "index.html", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/favicon.png"];
self.addEventListener("install", e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(CORE))); self.skipWaiting(); });
self.addEventListener("activate", e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k))))); self.clients.claim(); });
self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET") return;
  // Login e banco do Firebase nunca passam pelo cache.
  if (url.pathname.startsWith("/__/") || url.hostname.includes("googleapis.com") && !url.hostname.startsWith("fonts.")) return;
  if (req.mode === "navigate" || url.origin === location.origin) {
    e.respondWith(fetch(req).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return r; }).catch(() => caches.match(req).then(r => r || caches.match("index.html"))));
    return;
  }
  if (url.hostname === "www.gstatic.com" || url.hostname === "cdn.jsdelivr.net" || url.hostname.startsWith("fonts.")) {
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(r => { const copy = r.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return r; })));
  }
});
