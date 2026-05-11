document.addEventListener ('DOMContentLoaded', () => {
    const navToggle = document.querySelector('#navToggle');
    const navLinks = document.querySelector('#navLinks');

if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
     const isOpen = navLinks.classList.toggle('open');
    }
    );
}
});