(function () {
    'use strict';

    var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    /* ============ Animated counters ============ */
    function animateCounter(el) {
        var target = parseInt(el.getAttribute('data-count'), 10);
        var suffix = el.getAttribute('data-suffix') || '';

        if (isNaN(target)) return;

        if (reduceMotion) {
            el.textContent = target + suffix;
            return;
        }

        var current = 0;
        var steps = 40;

        var timer = setInterval(function () {
            current += target / steps;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            el.textContent = Math.round(current) + suffix;
        }, 40);
    }

    function isInViewport(el) {
        var rect = el.getBoundingClientRect();
        return rect.top < window.innerHeight && rect.bottom > 0;
    }

    var counters = document.querySelectorAll('[data-count]');
    var counted = [];

    function startCountersWhenVisible() {
        for (var i = 0; i < counters.length; i++) {
            var el = counters[i];
            if (counted.indexOf(el) === -1 && isInViewport(el)) {
                animateCounter(el);
                counted.push(el);
            }
        }
    }

    /* ============ Sticky header shadow + back to top ============ */
    var header = document.querySelector('.site-header');
    var backToTop = document.getElementById('back-to-top');

    function onScroll() {
        var scrolled = window.scrollY > 8;

        if (header) {
            header.classList.toggle('scrolled', scrolled);
        }

        if (backToTop) {
            backToTop.classList.toggle('show', window.scrollY > 400);
        }
    }

    if (backToTop) {
        backToTop.addEventListener('click', function () {
            window.scrollTo({
                top: 0,
                behavior: reduceMotion ? 'auto' : 'smooth'
            });
        });
    }

    /* ============ Close the mobile menu after choosing a link ============ */
    var navToggle = document.getElementById('nav-toggle');

    if (navToggle) {
        var navbar = document.getElementById('navbar');

        if (navbar) {
            navbar.addEventListener('click', function (e) {
                if (e.target.closest('a') || e.target.closest('button')) {
                    navToggle.checked = false;
                }
            });
        }

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') {
                navToggle.checked = false;
            }
        });
    }

    /* ============ Contact form: client-side feedback only ============ */
    var contactForm = document.getElementById('contact-form');

    if (contactForm) {
        var contactError = document.getElementById('contact-error');

        contactForm.addEventListener('submit', function (e) {
            e.preventDefault();

            if (!contactForm.checkValidity()) {
                if (contactError) {
                    contactError.textContent = 'Please fill in all fields with valid information.';
                }
                contactForm.reportValidity();
                return;
            }

            if (contactError) {
                contactError.textContent = '';
            }

            var button = contactForm.querySelector('button[type="submit"]');
            var original = button ? button.textContent : '';

            if (button) {
                button.disabled = true;
                button.textContent = 'Message sent — thank you!';
            }

            contactForm.reset();

            setTimeout(function () {
                if (button) {
                    button.disabled = false;
                    button.textContent = original;
                }
            }, 4000);
        });
    }

    window.addEventListener('scroll', function () {
        startCountersWhenVisible();
        onScroll();
    }, { passive: true });

    window.addEventListener('resize', onScroll);

    startCountersWhenVisible();
    onScroll();
})();