/*
 * RideEase Bike Rental System — Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function () {

    // Theme Toggle Logic
    const themeToggle = document.getElementById('themeToggle');
    const sunIcon     = document.getElementById('themeSunIcon');
    const moonIcon     = document.getElementById('themeMoonIcon');

    if (themeToggle && sunIcon && moonIcon) {
        function updateIcons(theme) {
            if (theme === 'dark') {
                sunIcon.style.setProperty('display', 'block', 'important');
                moonIcon.style.setProperty('display', 'none', 'important');
            } else {
                sunIcon.style.setProperty('display', 'none', 'important');
                moonIcon.style.setProperty('display', 'block', 'important');
            }
        }

        // Initial icon update based on active theme
        const activeTheme = document.documentElement.getAttribute('data-theme') || 'light';
        updateIcons(activeTheme);

        themeToggle.addEventListener('click', function () {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateIcons(newTheme);
        });
    }

    // Navbar scroll effect
    const navbar = document.getElementById('mainNavbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Auto-dismiss flash messages after 5 seconds
    const alerts = document.querySelectorAll('.flash-messages .alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Booking form — live cost calculation
    const pickupDate = document.getElementById('id_pickup_date');
    const returnDate = document.getElementById('id_return_date');

    if (pickupDate && returnDate) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        pickupDate.setAttribute('min', today);
        returnDate.setAttribute('min', today);

        function calcCost() {
            const p = new Date(pickupDate.value);
            const r = new Date(returnDate.value);
            if (!isNaN(p) && !isNaN(r) && r > p) {
                const days = Math.ceil((r - p) / (1000 * 60 * 60 * 24));
                const priceEl = document.getElementById('pricePerDay');
                const depositEl = document.getElementById('helmetDeposit');
                const totalEl = document.getElementById('totalCost');
                const daysEl = document.getElementById('totalDays');

                if (priceEl && totalEl) {
                    const rate    = parseFloat(priceEl.dataset.price) || 0;
                    const deposit = parseFloat(depositEl ? depositEl.dataset.deposit : 0) || 0;
                    const total   = (rate * days) + deposit;

                    if (daysEl) daysEl.textContent = days;
                    totalEl.textContent = '\u20b9' + total.toFixed(2);
                }
            }
        }

        pickupDate.addEventListener('change', function () {
            returnDate.setAttribute('min', this.value);
            calcCost();
        });
        returnDate.addEventListener('change', calcCost);
    }

    // Admin sidebar toggle (mobile)
    const sidebarToggle = document.getElementById('sidebarToggle');
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function () {
            const sidebar = document.getElementById('adminSidebar');
            const main    = document.querySelector('.admin-main');
            const topbar  = document.querySelector('.admin-topbar');
            if (sidebar) sidebar.classList.toggle('collapsed');
            if (main)    main.classList.toggle('expanded');
            if (topbar)  topbar.classList.toggle('expanded');
        });
    }

    // Confirm delete prompts
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Tooltip initialization
    const tooltipEls = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    tooltipEls.forEach(function (el) {
        new bootstrap.Tooltip(el);
    });

    // Image preview on file input
    const photoInput = document.querySelector('input[type="file"][accept="image/*"]');
    if (photoInput) {
        photoInput.addEventListener('change', function () {
            const file = this.files[0];
            if (!file) return;
            const preview = document.getElementById('photoPreview');
            if (preview) {
                preview.src = URL.createObjectURL(file);
                preview.classList.remove('d-none');
            }
        });
    }

});
