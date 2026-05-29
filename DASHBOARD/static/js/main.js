// ================= SLIDER DOTS =================
document.addEventListener('DOMContentLoaded', function() {
    const dots = document.querySelectorAll('.dot');
    let currentIndex = 0;
    
    if (dots.length > 0) {
        setInterval(() => {
            currentIndex = (currentIndex + 1) % 3;
            dots.forEach((dot, i) => {
                if (i === currentIndex) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }, 2000);
    }
});

// ================= UPDATE CART COUNT =================
function updateCartCount() {
    fetch('/get_cart_count/')
        .then(response => response.json())
        .then(data => {
            const cartCount = document.getElementById('cart-count');
            if (cartCount) {
                cartCount.textContent = data.count;
            }
        })
        .catch(error => console.log('Cart count error:', error));
}

// Load jumlah keranjang saat halaman dimuat
updateCartCount();