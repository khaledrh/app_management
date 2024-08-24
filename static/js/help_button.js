
    document.querySelectorAll('.help-button').forEach(function(button) {
        button.addEventListener('click', function() {
            const helptext = this.nextElementSibling;
            if (helptext.style.display === 'block') {
                helptext.style.display = 'none';
            } else {
                helptext.style.display = 'block';
            }
        });
    });
