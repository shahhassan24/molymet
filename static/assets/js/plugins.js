function loadScript(url, callback) {
    var script = document.createElement('script');
    script.type = 'application/javascript';
    script.src = url;
    script.onload = callback;
    script.onerror = function() {
        console.error('Failed to load script: ' + url);
    };
    document.head.appendChild(script);
}

// Check if any of the elements are present
if (document.querySelector("[toast-list]") || document.querySelector("[data-choices]") || document.querySelector("[data-provider]")) {
    loadScript('https://cdn.jsdelivr.net/npm/toastify-js', function() {
        console.log('Toastify-js loaded successfully');
    });
    loadScript('assets/libs/choices.js/public/assets/scripts/choices.min.js', function() {
        console.log('Choices.js loaded successfully');
    });
    loadScript('assets/libs/flatpickr/flatpickr.min.js', function() {
        console.log('Flatpickr loaded successfully');
    });
}
