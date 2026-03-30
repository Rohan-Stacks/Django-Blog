// Cache name
const CACHE_NAME = 'blog-pwa-v1';

// Core files to cache for offline usage
const APP_SHELL = [
  '/',
  '/about/',
  '/offline/',
  '/static/blog/main.css',
];

// Install event - caches core files
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

// Activate event - clean old caches
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.map(key => {
          if (key !== CACHE_NAME) return caches.delete(key);
        })
      )
    )
  );
  self.clients.claim();
});

// Fetch event - cache first for static files, network first for pages
self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Static assets: use cache first
  if (
    event.request.destination === 'style' ||
    event.request.destination === 'script' ||
    event.request.destination === 'image' ||
    url.pathname.startsWith('/static/')
  ) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        return cached || fetch(event.request).then(resp => {
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, resp.clone()));
          return resp;
        });
      })
    );
    return;
  }

  // Pages: network first, fallback to cache/offline
  event.respondWith(
    fetch(event.request)
      .then(resp => {
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, resp.clone()));
        return resp;
      })
      .catch(() => caches.match(event.request).then(cached => cached || caches.match('/offline/')))
  );
});