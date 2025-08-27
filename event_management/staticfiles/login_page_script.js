// Elements
const loginBtn = document.querySelector(".login-btn");
const formPopup = document.querySelector(".form-popup");
const blurOverlay = document.querySelector(".blur-bg-overlay");
const closeBtn = document.querySelector(".form-popup .close-btn");

// Switch forms
const signupLink = document.querySelector("#signup-link");
const loginLink = document.querySelector("#login-link");
const loginForm = document.querySelector(".form-box.login");
const signupForm = document.querySelector(".form-box.signup");

// Open popup
loginBtn.addEventListener("click", () => {
    formPopup.classList.add("active");
    blurOverlay.classList.add("active");
    loginForm.style.display = "block";
    signupForm.style.display = "none";
});

// Close popup
closeBtn.addEventListener("click", () => {
    formPopup.classList.remove("active");
    blurOverlay.classList.remove("active");
});

// Close on overlay click
blurOverlay.addEventListener("click", () => {
    formPopup.classList.remove("active");
    blurOverlay.classList.remove("active");
});

// Switch to Signup
signupLink.addEventListener("click", (e) => {
    e.preventDefault();
    loginForm.style.display = "none";
    signupForm.style.display = "block";
});

// Switch to Login
loginLink.addEventListener("click", (e) => {
    e.preventDefault();
    signupForm.style.display = "none";
    loginForm.style.display = "block";
});

function sendOtp() {
    let email = document.getElementById("forgot-email").value;
    if (!email) {
        alert("Please enter your registered email.");
        return;
    }

    fetch("{% url 'send_otp' %}", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": "{{ csrf_token }}"
        },
        body: `email=${encodeURIComponent(email)}`
    })

    .then(response => response.json())
    .then(data => {
        alert(data.message);
        if (data.status === "success") {
            document.getElementById("reset-form").style.display = "block";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Something went wrong. Please try again.");
    });
}
