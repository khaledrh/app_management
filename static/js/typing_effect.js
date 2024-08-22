document.addEventListener("DOMContentLoaded", function() {
    const textElement = document.getElementById("animated-text");
    const textContent = textElement.textContent;
    textElement.textContent = '';  // Clear the initial text

    let index = 0;
    function typeLetter() {
        if (index < textContent.length) {
            textElement.textContent += textContent.charAt(index);
            index++;
            setTimeout(typeLetter, 100);  // Adjust the speed by changing the delay
        } else {
            textElement.classList.remove('hidden');  // Reveal the full text
        }
    }

    typeLetter();  // Start the typing effect
});