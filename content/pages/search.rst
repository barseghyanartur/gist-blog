Search
======

.. raw:: html

   <style>
     .search-container { max-width: 800px; margin: 2rem auto; }
     #search-input { width: 100%; padding: 1rem; font-size: 1.2rem; border: 2px solid #ddd; border-radius: 8px; }
     #search-results ul { list-style: none; padding: 0; }
     #search-results li { margin: 1rem 0; padding: 1rem; border: 1px solid #eee; border-radius: 8px; }
     #search-results a { font-size: 1.3rem; text-decoration: none; }
   </style>

   <div class="search-container">
     <input type="text" id="search-input" placeholder="Search posts by title, content, tags..." onkeyup="performSearch()">
     <div id="search-results"></div>
   </div>

   <script src="https://cdnjs.cloudflare.com/ajax/libs/lunr/2.3.9/lunr.min.js"></script>
   <script>
     let idx, postsData;
     async function loadIndex() {
       const resp = await fetch('/static/search_index.json');
       postsData = await resp.json();
       idx = lunr(function () {
         this.ref('url');
         this.field('title', { boost: 10 });
         this.field('content');
         this.field('category');
         this.field('tags');
         postsData.forEach(doc => this.add(doc));
       });
     }
     function performSearch() {
       const query = document.getElementById('search-input').value.trim();
       const container = document.getElementById('search-results');
       if (!query || !idx) { container.innerHTML = ''; return; }
       const results = idx.search(query);
       let html = '<ul>';
       results.forEach(res => {
         const post = postsData.find(p => p.url === res.ref);
         if (post) {
           html += `<li><a href="${post.url}">${post.title}</a><br>
                    <small>${post.date} • ${post.category} • ${post.tags.join(', ')}</small></li>`;
         }
       });
       html += '</ul>';
       container.innerHTML = results.length ? html : '<p>No results found.</p>';
     }
     window.onload = loadIndex;
   </script>
