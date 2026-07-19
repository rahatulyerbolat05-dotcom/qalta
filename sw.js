/* Қалта — офлайн-кэш v1
   - index.html / навигация → сначала сеть, офлайн — из кэша (обновления доезжают сами)
   - иконки/манифест/фотообои → сначала кэш (не меняются)
   - запросы к script.google.com не трогаем вовсе (синхронизация)
*/
var CACHE='qalta-v1';
var PRECACHE=['./','./index.html','./manifest.json','./icon-180.png','./icon-512.png',
  './wp_manor.jpg','./wp_lagoon.jpg','./wp_dusk.jpg','./wp_vangogh.jpg','./wp_barkhan.jpg','./wp_mirage.jpg','./wp_bloom.jpg'];

self.addEventListener('install',function(e){
  e.waitUntil(
    caches.open(CACHE).then(function(c){
      return Promise.all(PRECACHE.map(function(u){ return c.add(u).catch(function(){}); }));
    }).then(function(){ return self.skipWaiting(); })
  );
});

self.addEventListener('activate',function(e){
  e.waitUntil(caches.keys().then(function(keys){
    return Promise.all(keys.filter(function(k){ return k!==CACHE; }).map(function(k){ return caches.delete(k); }));
  }).then(function(){ return self.clients.claim(); }));
});

function networkFirst(req){
  return fetch(req).then(function(res){
    if(res && res.ok){
      var copy=res.clone();
      caches.open(CACHE).then(function(c){ c.put(req,copy); });
    }
    return res;
  }).catch(function(){
    return caches.match(req,{ignoreSearch:true}).then(function(hit){
      if(hit) return hit;
      if(req.mode==='navigate') return caches.match('./index.html');
      throw new Error('offline');
    });
  });
}

self.addEventListener('fetch',function(e){
  if(e.request.method!=='GET') return;
  var url=e.request.url.split('?')[0];
  if(url.indexOf(self.location.origin)!==0) return; /* Google Apps Script и прочее — мимо кэша */

  if(e.request.mode==='navigate' || /\/(index\.html)$/.test(url) || /\/$/.test(url)){
    e.respondWith(networkFirst(e.request));
    return;
  }
  e.respondWith(
    caches.match(e.request,{ignoreSearch:true}).then(function(hit){
      if(hit) return hit;
      return fetch(e.request).then(function(res){
        if(res && res.ok){
          var copy=res.clone();
          caches.open(CACHE).then(function(c){ c.put(e.request,copy); });
        }
        return res;
      });
    })
  );
});
