document.addEventListener('DOMContentLoaded', function() {

    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }

        if (scrollTop > lastScrollTop && scrollTop > 100) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }

        lastScrollTop = scrollTop;
    });

    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });

        input.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });

        if (input.value) {
            input.parentElement.classList.add('focused');
        }
    });

    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const inputs = form.querySelectorAll('.form-control[required]');
            let isValid = true;

            inputs.forEach(input => {
                if (!input.value.trim()) {
                    input.classList.add('is-invalid');
                    isValid = false;
                } else {
                    input.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                const firstInvalid = form.querySelector('.is-invalid');
                if (firstInvalid) {
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstInvalid.focus();
                }
            }
        });
    });

    document.querySelectorAll('.room-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        const checkInInput = searchForm.querySelector('input[name*="check_in"]');
        const checkOutInput = searchForm.querySelector('input[name*="check_out"]');

        if (checkInInput && checkOutInput) {
            checkInInput.addEventListener('change', function() {
                const checkInDate = new Date(this.value);
                const today = new Date();

                if (checkInDate < today) {
                    this.setCustomValidity('Check-in date must be in the future');
                } else {
                    this.setCustomValidity('');
                }

                checkOutInput.min = this.value;
            });

            checkOutInput.addEventListener('change', function() {
                const checkInDate = new Date(checkInInput.value);
                const checkOutDate = new Date(this.value);

                if (checkOutDate <= checkInDate) {
                    this.setCustomValidity('Check-out date must be after check-in date');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
    }

    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.transition = 'opacity 0.5s ease';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        }, 5000);
    });
});

function confirmDelete(message) {
    return confirm(message || 'هل أنت متأكد من هذا الإجراء؟');
}

function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>جاري التحميل...';
    button.disabled = true;

    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 2000);
}
