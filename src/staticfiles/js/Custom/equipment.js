document.addEventListener("DOMContentLoaded", function () {
  const dynamicModal = document.querySelector("#dynamicModal");
  const modalBody = document.querySelector(".modal-body");
  const modalTitle = document.querySelector("#modalTitle");

  const defineModalTitle = (action, type) => {
    const actionText =
      {
        add: "Ajouter",
        edit: "Modifier",
        delete: "Supprimer",
      }[action] || "Action";

    const typeText =
      {
        telescope: "Télescope",
        camera: "Caméra",
      }[type] || "Équipement";

    return `${actionText} ${typeText}`;
  };

  const handleFormErrors = (errors) => {
    document
      .querySelectorAll(".text-danger")
      .forEach((el) => (el.innerHTML = ""));

    for (let field in errors) {
      let errorMessage = errors[field][0].message;
      let errorDiv = document.querySelector(`#error-${field}`);

      if (errorDiv) {
        errorDiv.innerHTML = errorMessage;
      }
    }
  };

  const clearFormErrors = () => {
    document
      .querySelectorAll(".text-danger")
      .forEach((el) => (el.innerHTML = ""));
  };

  // Handle opening of the modal
  dynamicModal.addEventListener("show.bs.modal", function (event) {
    const button = event.relatedTarget;
    const url = button?.getAttribute("data-url");
    const action = button?.getAttribute("data-action");
    const type = button?.getAttribute("data-type");

    // Ensure button or URL is defined and valid
    if (!button || !url) {
      console.error("Bouton ou URL non définis.");
      return;
    }

    modalTitle.textContent = defineModalTitle(action, type);

    // Fetch form content
    fetch(url)
      .then((response) => response.text())
      .then((html) => {
        modalBody.innerHTML = html;
      })
      .catch((error) => {
        console.error("Erreur lors du chargement du formulaire :", error);
        modalBody.innerHTML =
          '<p class="text-danger">Erreur lors du chargement du formulaire.</p>';
      });
  });

  // Handle form submission
  dynamicModal.addEventListener("submit", function (event) {
    event.preventDefault();

    const form = event.target;
    const url = form.action;
    const formData = new FormData(form);
    const action = form.getAttribute("data-action");
    const equipmentId = form.getAttribute("data-equipment-id");

    //console.log(form);
    //console.log(url);

    clearFormErrors();

    // Specific case for deletion form
    if (action === "delete") {
      fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Erreur réseau");
          }
          response.json();
        })
        .then((data) => {
          if (data.success) {
            console.log("Équipement supprimé avec succès");
            const modalInstance = bootstrap.Modal.getInstance(dynamicModal);
            modalInstance.hide();

            console.log(formData);
            console.log(action);
            console.log(equipmentId);

            // Wait 500ms for a smooth transition
            setTimeout(() => {
              const equipmentRow = document.getElementById(
                `equipment-${equipmentId}`
              );
              if (equipmentRow) {
                equipmentRow.remove();
              }
            }, 500);
          } else {
            console.log("Erreur lors de la suppression");
            modalBody.innerHTML =
              '<p class="text-danger">Erreur lors de la suppression</p>';
          }
        })
        .catch((error) => {
          console.error("Erreur lors de la suppression :", error);
          modalBody.innerHTML =
            '<p class="text-danger">Erreur technique, veuillez réessayer.</p>';
        });

      return;
    }

    // Generic case for add/edit form
    fetch(url, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data.success) {
          console.log("Formulaire correctement soumis");
          const modalInstance = bootstrap.Modal.getInstance(dynamicModal);
          modalInstance.hide();

          console.log(formData);
          console.log(action);
          console.log(equipmentId);

          // Wait 500ms for a smooth transition
          setTimeout(() => {
            location.reload();
          }, 500);
        } else {
          console.log("Le formulaire contient des erreurs.");
          handleFormErrors(data.errors);
        }
      })
      .catch((error) => {
        console.error("Erreur lors de la soumission du formulaire :", error);
        modalBody.innerHTML =
          '<p class="text-danger">Erreur lorsssss de la soumission du formulaire.</p>';
      });
  });
});
