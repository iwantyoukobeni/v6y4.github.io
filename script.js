function showEndpoint(endpoint) {
    var section = document.getElementById(endpoint);
    var button = document.querySelector('.api-button');

    if (section.classList.contains('hidden')) {
        section.classList.remove('hidden');
        button.classList.add('clicked');

        // Remove the 'clicked' class after a short delay (300ms)
        setTimeout(function() {
            button.classList.remove('clicked');
        }, 300);
    } else {
        section.classList.add('hidden');
    }
}
