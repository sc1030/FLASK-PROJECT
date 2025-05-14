/**
 * Sentiment Analysis App - Custom JavaScript
 */

// Document ready function
document.addEventListener('DOMContentLoaded', function() {
    
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            if (alert) {
                alert.style.opacity = '0';
                alert.style.transition = 'opacity 1s';
                setTimeout(function() {
                    if (alert && alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 1000);
            }
        }, 5000);
    });

    // Validate search form submission
    const analyzeForm = document.querySelector('form[action*="sentiment_analyzer"]');
    if (analyzeForm) {
        analyzeForm.addEventListener('submit', function(event) {
            const searchTerm = document.getElementById('search_term').value.trim();
            if (!searchTerm) {
                event.preventDefault();
                alert('Please enter a search term or hashtag.');
                return false;
            }
            
            // Show loading spinner
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Analyzing...';
                submitBtn.disabled = true;
            }
            
            return true;
        });
    }

    // Confirm logout
    const logoutLink = document.querySelector('a[href*="logout"]');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(event) {
            if (!confirm('Are you sure you want to log out?')) {
                event.preventDefault();
                return false;
            }
            return true;
        });
    }
    
    // Tooltip initialization (requires Bootstrap's tooltip.js)
    if (typeof jQuery !== 'undefined' && typeof jQuery().tooltip === 'function') {
        jQuery('[data-toggle="tooltip"]').tooltip();
    }
    
    // Password strength meter (optional feature)
    const passwordInput = document.getElementById('password');
    const strengthMeter = document.getElementById('password-strength');
    
    if (passwordInput && strengthMeter) {
        passwordInput.addEventListener('input', function() {
            const password = this.value;
            let strength = 0;
            
            if (password.length >= 8) strength += 1;
            if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength += 1;
            if (password.match(/\d/)) strength += 1;
            if (password.match(/[^a-zA-Z\d]/)) strength += 1;
            
            switch(strength) {
                case 0:
                    strengthMeter.style.width = '0%';
                    strengthMeter.className = 'progress-bar';
                    break;
                case 1:
                    strengthMeter.style.width = '25%';
                    strengthMeter.className = 'progress-bar bg-danger';
                    break;
                case 2:
                    strengthMeter.style.width = '50%';
                    strengthMeter.className = 'progress-bar bg-warning';
                    break;
                case 3:
                    strengthMeter.style.width = '75%';
                    strengthMeter.className = 'progress-bar bg-info';
                    break;
                case 4:
                    strengthMeter.style.width = '100%';
                    strengthMeter.className = 'progress-bar bg-success';
                    break;
            }
        });
    }
});