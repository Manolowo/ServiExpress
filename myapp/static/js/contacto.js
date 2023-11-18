document.addEventListener("DOMContentLoaded", function () {
  const contactoLink = document.querySelector('.nav-items li a[href="#contact-form"]');
  if (contactoLink) {
    contactoLink.addEventListener("click", function (event) {
      event.preventDefault();
      document.getElementById("contact-form").scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });
  }

  // Verifica si jQuery está definido antes de utilizarlo
  if (typeof jQuery !== 'undefined') {
    const contactForm = document.getElementById("contact-form");
    if (contactForm) {
      contactForm.addEventListener("submit", function (event) {
        event.preventDefault();

        const name = document.getElementById("fname").value;
        const email = document.getElementById("femail").value;
        const message = document.getElementById("message").value;

        if (name && email && message) {
          $.ajax({
            url: contactForm.getAttribute("action"),
            type: contactForm.getAttribute("method"),
            data: $(contactForm).serialize(),
            success: function (response) {
              Swal.fire({
                title: "Nos hemos puesto en contacto",
                text: "Nos pondremos en contacto contigo en breve.",
                icon: "success",
                confirmButtonText: "Aceptar",
              });
            },
            error: function (error) {
              console.error(error);
            },
          });
        } else {
          Swal.fire({
            title: "¡Error!",
            text: "Todos los campos son obligatorios",
            icon: "error",
            confirmButtonText: "Aceptar",
          });
        }
      });
    }
  } else {
    console.error("jQuery no está definido. Asegúrate de cargar jQuery antes de tu script.");
  }
});
