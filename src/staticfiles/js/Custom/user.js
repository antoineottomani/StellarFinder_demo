document.getElementById("signupForm").addEventListener(
  "submit",
  function (event) {
    //const form = event.target;
    const username = document.getElementById("id_username").value;
    const email = document.getElementById("id_email").value;
    const password1 = document.getElementById("id_password1").value;
    const password2 = document.getElementById("id_password2").value;
    let valid = true;

    // Clear previous error messages
    document.getElementById("usernameError").textContent = "";
    document.getElementById("emailError").textContent = "";
    document.getElementById("password1Error").textContent = "";
    document.getElementById("password2Error").textContent = "";

    // Vérification du pseudo
    if (username.length < 6 || username.length > 12) {
      valid = false;
      document.getElementById("usernameError").textContent =
        "Le pseudo doit contenir entre 6 et 12 caractères.";
    }
    if (!/^[a-zA-Z0-9]+$/.test(username)) {
      valid = false;
      document.getElementById("usernameError").textContent +=
        " Le pseudo ne peut contenir que des lettres et des chiffres.";
    }

    // Vérification de l'email
    if (email === "") {
      valid = false;
      document.getElementById("emailError").textContent =
        "L'adresse email ne peut pas être vide.";
    }

    // Vérification du mot de passe
    if (password1.length < 8) {
      valid = false;
      document.getElementById("password1Error").textContent =
        "Votre mot de passe doit contenir 8 caractères minimum.";
    }
    if (!/[A-Z]/.test(password1)) {
      valid = false;
      document.getElementById("password1Error").textContent +=
        " Votre mot de passe doit contenir au moins une lettre majuscule.";
    }
    if (!/[a-z]/.test(password1)) {
      valid = false;
      document.getElementById("password1Error").textContent +=
        " Votre mot de passe doit contenir au moins une lettre minuscule.";
    }
    if (!/[0-9]/.test(password1)) {
      valid = false;
      document.getElementById("password1Error").textContent +=
        " Votre mot de passe doit contenir au moins un chiffre.";
    }
    if (!/[\W_]/.test(password1)) {
      valid = false;
      document.getElementById("password1Error").textContent +=
        " Votre mot de passe doit contenir au moins un caractère spécial.";
    }

    // Vérification de la correspondance des mots de passe
    if (password1 !== password2) {
      valid = false;
      document.getElementById("password2Error").textContent =
        "Les mots de passe ne correspondent pas.";
    }

    if (!valid) {
      event.preventDefault();
      event.stopPropagation();
    }

    //form.classList.add('was-validated');
  },
  false
);
