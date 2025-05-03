document.querySelector('#app').innerHTML = '<h1>Welcome to the Modern Flask App</h1>'; 

const navbarToggle = document.querySelector('#navbar-toggle');
const navbarMenu = document.querySelector('#navbar-menu');

navbarToggle.addEventListener('click', () => {
    navbarMenu.classList.toggle('hidden');
});

window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    header.classList.toggle('scrolled', window.scrollY > 0);
});