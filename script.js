// Messaggio di benvenuto
function showMessage() {
    alert('🎮 Benvenuto in Kebuy Studios! La tua casa di giochi.');
}

// Contatore giorni online
function updateCounter() {
    const startDate = new Date('2026-03-18'); // Data di lancio
    const today = new Date();
    const diffTime = today - startDate;
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    const counterEl = document.getElementById('online-counter');
    if (counterEl) {
        counterEl.textContent = `🎉 Online da ${diffDays} giorni!`;
    }
}

// Esegui quando la pagina è caricata
document.addEventListener('DOMContentLoaded', function() {
    updateCounter();
    
    // Effetto extra sul logo
    const logo = document.getElementById('site-logo');
    if (logo) {
        logo.addEventListener('mouseenter', () => {
            logo.style.transform = 'scale(1.1) rotate(5deg)';
            logo.style.transition = '0.3s';
        });
        logo.addEventListener('mouseleave', () => {
            logo.style.transform = 'scale(1) rotate(0)';
        });
    }
});
