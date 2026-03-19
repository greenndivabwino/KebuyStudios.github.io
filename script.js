// Kebuy Studios - JavaScript

// Effetto di benvenuto nella console
console.log('🎮 Benvenuto in Kebuy Studios! Il nostro quartier generale digitale.');

// Gestione header trasparente allo scroll
window.addEventListener('scroll', function() {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.style.background = 'rgba(6, 6, 10, 0.95)';
    } else {
        header.style.background = 'rgba(6, 6, 10, 0.8)';
    }
});

// Aggiunge classe active al link corrente
document.addEventListener('DOMContentLoaded', function() {
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href');
        if (linkPage === currentPage) {
            link.classList.add('active');
        } else if (currentPage === '' && linkPage === 'index.html') {
            link.classList.add('active');
        }
    });
});
