/* ==========================================
   RISING WATERS - GLOBAL JAVASCRIPT
========================================== */

// ===============================
// PRELOADER
// ===============================

window.addEventListener("load", function () {

    const loader = document.getElementById("preloader");

    if (loader) {
        loader.style.opacity = "0";

        setTimeout(() => {
            loader.style.display = "none";
        }, 500);
    }

});

// ===============================
// SCROLL PROGRESS BAR
// ===============================

window.addEventListener("scroll", function () {

    const progress = document.getElementById("progress-bar");

    if (!progress) return;

    const scrollTop = document.documentElement.scrollTop;
    const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;

    const percent = (scrollTop / height) * 100;

    progress.style.width = percent + "%";

});

// ===============================
// BACK TO TOP BUTTON
// ===============================

const topBtn = document.getElementById("topBtn");

window.addEventListener("scroll", function () {

    if (!topBtn) return;

    if (window.scrollY > 300) {

        topBtn.style.display = "block";

    } else {

        topBtn.style.display = "none";

    }

});

if (topBtn) {

    topBtn.addEventListener("click", function () {

        window.scrollTo({

            top: 0,
            behavior: "smooth"

        });

    });

}

// ===============================
// NAVBAR SHADOW
// ===============================

window.addEventListener("scroll", function () {

    const nav = document.querySelector(".navbar");

    if (!nav) return;

    if (window.scrollY > 30) {

        nav.style.boxShadow = "0 5px 20px rgba(0,0,0,.15)";

    } else {

        nav.style.boxShadow = "none";

    }

});

// ===============================
// ACTIVE NAVIGATION LINK
// ===============================

const current = window.location.pathname;

document.querySelectorAll(".nav-link").forEach(link => {

    if (link.getAttribute("href") === current) {

        link.classList.add("active");

    }

});

// ===============================
// DARK MODE
// ===============================

const themeBtn = document.getElementById("theme-toggle");

if (themeBtn) {

    themeBtn.addEventListener("click", function () {

        document.body.classList.toggle("dark-mode");

        if (document.body.classList.contains("dark-mode")) {

            localStorage.setItem("theme", "dark");

            themeBtn.innerHTML =
                '<i class="fas fa-sun"></i>';

        }

        else {

            localStorage.setItem("theme", "light");

            themeBtn.innerHTML =
                '<i class="fas fa-moon"></i>';

        }

    });

}

// Load Theme

window.onload = function () {

    if (localStorage.getItem("theme") === "dark") {

        document.body.classList.add("dark-mode");

        if (themeBtn)
            themeBtn.innerHTML =
                '<i class="fas fa-sun"></i>';

    }

};

// ===============================
// CARD HOVER EFFECT
// ===============================

document.querySelectorAll(".card").forEach(card => {

    card.addEventListener("mouseenter", function () {

        card.style.transform = "translateY(-6px)";

    });

    card.addEventListener("mouseleave", function () {

        card.style.transform = "translateY(0px)";

    });

});

// ===============================
// FORM VALIDATION
// ===============================

document.querySelectorAll("form").forEach(form => {

    form.addEventListener("submit", function () {

        const btn = form.querySelector("button[type='submit']");

        if (btn) {

            btn.disabled = true;

            btn.innerHTML =
                '<i class="fas fa-spinner fa-spin"></i> Please Wait...';

        }

    });

});

// ===============================
// AUTO CLOSE ALERTS
// ===============================

setTimeout(function () {

    document.querySelectorAll(".alert").forEach(alert => {

        alert.style.transition = ".5s";

        alert.style.opacity = "0";

        setTimeout(() => {

            alert.remove();

        }, 500);

    });

}, 4000);

// ===============================
// AOS INIT
// ===============================

if (typeof AOS !== "undefined") {

    AOS.init({

        duration: 1000,
        once: true

    });

}

console.log("🌊 Rising Waters Loaded Successfully");