// ============================================
// ORBIT — Base JavaScript
// ============================================

// Subtle parallax on blob movement based on mouse
document.addEventListener('mousemove', (e) => {
    const blobs = document.querySelectorAll('.blob');
    const x = (e.clientX / window.innerWidth - 0.5) * 20;
    const y = (e.clientY / window.innerHeight - 0.5) * 20;

    blobs.forEach((blob, i) => {
        const factor = (i + 1) * 0.4;
        blob.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
    });
});

// Flash message auto-dismiss
document.querySelectorAll('.flash-message').forEach(msg => {
    setTimeout(() => {
        msg.style.opacity = '0';
        msg.style.transform = 'translateY(-10px)';
        setTimeout(() => msg.remove(), 300);
    }, 4000);
});

// Animate elements in on load
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-animate]').forEach((el, i) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(16px)';
        el.style.transition = `opacity 0.5s ease ${i * 0.08}s, transform 0.5s ease ${i * 0.08}s`;
        requestAnimationFrame(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        });
    });
});