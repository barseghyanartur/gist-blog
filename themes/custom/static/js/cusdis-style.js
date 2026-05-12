(function () {
    var CUSTOM_CSS =
        'html{font-size:12px}' +
        'body{font-family:"Trebuchet MS",Trebuchet,"Lucida Sans Unicode","Lucida Grande","Lucida Sans",Arial,sans-serif;color:#000305}' +
        'input,textarea,button,label{font-family:inherit}' +
        '.w-full.p-2{padding:3px 6px!important}' +
        '.h-24{height:3rem!important}' +
        '.gap-4{gap:0.5rem!important}' +
        '.text-gray-500{color:#888!important}';

    var desc = Object.getOwnPropertyDescriptor(HTMLIFrameElement.prototype, 'srcdoc');
    if (!desc || !desc.set) return;

    Object.defineProperty(HTMLIFrameElement.prototype, 'srcdoc', {
        configurable: true,
        get: desc.get,
        set: function (value) {
            if (typeof value === 'string' && value.indexOf('CUSDIS_LOCALE') !== -1) {
                value = value.replace('</head>', '<style>' + CUSTOM_CSS + '</style></head>');
                Object.defineProperty(HTMLIFrameElement.prototype, 'srcdoc', desc);
            }
            desc.set.call(this, value);
        }
    });
}());
