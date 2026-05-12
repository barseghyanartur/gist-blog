(function () {
    var CSS = [
        'html { font-size: 12px; }',
        'body {',
        '  font-family: "Trebuchet MS", Trebuchet, "Lucida Sans Unicode", "Lucida Grande", "Lucida Sans", Arial, sans-serif;',
        '  color: #000305;',
        '}',
        'input, textarea, button, label, p, span, a { font-family: inherit; }',
        /* compact input padding */
        '.w-full.p-2 { padding: 3px 6px !important; }',
        /* shorter textarea */
        '.h-24 { height: 3rem !important; }',
        /* tighter grid gap between name/email columns */
        '.gap-4 { gap: 0.5rem !important; }',
        /* mute label colour to match blog metadata */
        '.text-gray-500 { color: #888 !important; }',
        /* submit button compact */
        '.bg-blue-500 { padding: 3px 10px !important; font-size: 0.75rem !important; }',
    ].join('\n');

    function inject(iframe) {
        function applyStyles() {
            try {
                var doc = iframe.contentDocument || iframe.contentWindow.document;
                var style = doc.createElement('style');
                style.textContent = CSS;
                doc.head.appendChild(style);
            } catch (e) {}
        }
        if (iframe.contentDocument && iframe.contentDocument.readyState === 'complete') {
            applyStyles();
        } else {
            iframe.addEventListener('load', applyStyles);
        }
    }

    function watch() {
        var thread = document.getElementById('cusdis_thread');
        if (!thread) return;
        var existing = thread.querySelector('iframe');
        if (existing) { inject(existing); return; }
        var observer = new MutationObserver(function (mutations) {
            for (var i = 0; i < mutations.length; i++) {
                var nodes = mutations[i].addedNodes;
                for (var j = 0; j < nodes.length; j++) {
                    if (nodes[j].tagName === 'IFRAME') {
                        observer.disconnect();
                        inject(nodes[j]);
                        return;
                    }
                }
            }
        });
        observer.observe(thread, { childList: true });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', watch);
    } else {
        watch();
    }
}());
