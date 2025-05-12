document.addEventListener('DOMContentLoaded', function () {
    // Flashcard flip functionality
    const flashcards = document.querySelectorAll('.flashcard');
    flashcards.forEach(card => {
        card.addEventListener('click', function () {
            const cardInner = this.querySelector('.flashcard-inner');
            if (cardInner) {
                cardInner.classList.toggle('is-flipped');
            }
        });
    });

    // Delete deck confirmation
    const deleteDeckForms = document.querySelectorAll('.delete-deck-form');
    deleteDeckForms.forEach(form => {
        form.addEventListener('submit', function(event) {
            const deckTitle = this.closest('.bg-white').querySelector('h2').textContent || "this deck";
            const confirmation = window.confirm(`Are you sure you wish to delete the deck "${deckTitle}"? This action cannot be undone.`);
            if (!confirmation) {
                event.preventDefault(); // Stop form submission if user cancels
            }
            // If confirmed, the form will submit as normal
        });
    });

    // Mobile menu toggle (if you have one, example below)
    const menuButton = document.querySelector('.mobile-menu-button'); // Adjust selector if needed
    const mobileMenu = document.querySelector('.mobile-menu'); // Adjust selector if needed

    if (menuButton && mobileMenu) {
        menuButton.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Dismiss flash messages
    const flashMessages = document.querySelectorAll('.flash-message-dismiss');
    flashMessages.forEach(function(button) {
        button.addEventListener('click', function() {
            this.closest('.flash-message').style.display = 'none';
        });
    });

    // Add more interactive JS as needed
});

const navbarToggle = document.querySelector('#navbar-toggle');
const navbarMenu = document.querySelector('#navbar-menu');

if (navbarToggle && navbarMenu) {
    navbarToggle.addEventListener('click', () => {
        navbarMenu.classList.toggle('hidden');
    });
}

window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (header) {
        header.classList.toggle('scrolled', window.scrollY > 0);
    }
});