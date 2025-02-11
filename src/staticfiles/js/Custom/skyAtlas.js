let aladin;
let fovOverlay;

// Initialisation d'Aladin et ajout de l'événement de recherche
A.init.then(() => {
  aladin = A.aladin("#aladin-lite-div", {
    survey: "P/Mellinger/color", // Survey pour afficher la Voie Lactée
    fov: 80, // Champ de vision en degrés pour inclure une large portion de la Voie Lactée
    target: "IC4604",
    showFov: false,
    cooFrame: false,
    showCooGridControl: false,
    showShareControl: false,
    showControlPanel: false,
    showLayersControl: false,
    expandLayersControl: false,
    showFullscreenControl: false,
    showSimbadPointerControl: false,
    showSettingsControl: false,
    showStatusBar: false,
    showFrame: false,
    showProjectionControl: false,
    showCooLocation: false,
    showCooGrid: false,
  });

  fovOverlay = A.graphicOverlay({ color: "red", lineWidth: 2 });
  aladin.addOverlay(fovOverlay);

  document
    .querySelector(".search-target-btn")
    .addEventListener("click", searchTarget);
});

// Fonction de recherche d'un astre
function searchTarget(event) {
  event.preventDefault();

  let targetName = document.getElementById("search-input").value.trim();
  const isUserAuthenticated = document.getElementById("userEquipment") !== null;

  if (isUserAuthenticated) {
    let telescopeId = document.getElementById("telescopes").value;
    let cameraId = document.getElementById("cameras").value;

    if (!targetName || !telescopeId || !cameraId) {
      displayError("Veuillez remplir tous les champs requis.");
      return;
    }

    clearError();
    aladin.gotoObject(targetName, {
      success: (raDec) => {
        if (raDec) {
          console.log(`Astre ${targetName} trouvé avec succès.`);
          // Changer de survey pour un affichage détaillé
          aladin.setImageSurvey("P/DSS2/color");
          fovOverlay.removeAll();

          fetchFov(telescopeId, cameraId, targetName);
        } else {
          displayError(
            `La recherche pour l'astre ${targetName} n'a rien donné`
          );
        }
      },
      error: (err) => {
        console.error(
          `Erreur lors de la recherche pour l'astre ${targetName}:`,
          err
        );
        displayError(`La recherche pour l'astre ${targetName} n'a rien donné`);
      },
    });
  } else {
    if (!targetName) {
      displayError("Veuillez entrer un nom d'astre.");
      return;
    }

    clearError();
    aladin.gotoObject(targetName, {
      success: (raDec) => {
        if (raDec) {
          console.log(`Astre ${targetName} trouvé avec succès.`);
          // Changer de survey pour un affichage détaillé
          aladin.setImageSurvey("P/DSS2/color");
          adjustZoomForUnauthenticatedUser(raDec);
        } else {
          displayError(
            `La recherche pour l'astre ${targetName} n'a rien donné`
          );
        }
      },
      error: (err) => {
        console.error(
          `Erreur lors de la recherche pour l'astre ${targetName}:`,
          err
        );
        displayError(`La recherche pour l'astre ${targetName} n'a rien donné`);
      },
    });
  }
}

function adjustZoomForUnauthenticatedUser(raDec) {
  const defaultFovRadius = 4; // Exemple de FOV par défaut en degrés

  const ra = raDec[0];
  const dec = raDec[1];

  aladin.setFoV(defaultFovRadius);
  aladin.gotoRaDec(ra, dec);
}

// Fonction pour dessiner un rectangle représentant le FOV
function drawFovRectangle(fovWidth, fovHeight, targetName) {
  fovOverlay.removeAll(); // Supprimer tous les anciens polygones
  // let fovOverlay = aladin.getOverlay('fovOverlay');
  // if (!fovOverlay) {
  //     fovOverlay = A.graphicOverlay({name: 'fovOverlay', color: 'red', lineWidth: 2});
  //     aladin.addOverlay(fovOverlay);
  // } else {
  //     fovOverlay.removeAll();
  // }

  aladin.gotoObject(targetName, {
    success: (raDec) => {
      if (raDec) {
        const ra = raDec[0];
        const dec = raDec[1];

        const rectangle = A.polyline(
          [
            [ra - fovWidth / 2, dec - fovHeight / 2],
            [ra + fovWidth / 2, dec - fovHeight / 2],
            [ra + fovWidth / 2, dec + fovHeight / 2],
            [ra - fovWidth / 2, dec + fovHeight / 2],
            [ra - fovWidth / 2, dec - fovHeight / 2],
          ],
          { color: "green", lineWidth: 1 }
        );

        fovOverlay.addFootprints([rectangle]);

        const fovRadius = Math.max(fovWidth, fovHeight);
        aladin.setFoV(fovRadius * 1.5);
        aladin.gotoRaDec(ra, dec);

        document.getElementById("fov-width").value = fovWidth;
        document.getElementById("fov-height").value = fovHeight;
      } else {
        displayError(
          `Erreur lors de la mise à jour du champ de vision pour ${targetName}.`
        );
      }
    },
    error: (err) => {
      displayError(
        `Erreur lors de la mise à jour du champ de vision pour ${targetName}.`
      );
    },
  });
}

// Fonction pour récupérer le champ de vision (FOV)
function fetchFov(telescopeId, cameraId, targetName) {
  const url = `/calcul-fov/${telescopeId}/${cameraId}/`;

  fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    credentials: "include",
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "success") {
        const fovWidth = data.data.fov_width;
        const fovHeight = data.data.fov_height;
        drawFovRectangle(fovWidth, fovHeight, targetName);

        document.querySelector("#fov-width").value = fovWidth;
        document.querySelector("#fov-height").value = fovHeight;
      } else {
        displayError("Erreur lors du calcul du FOV.");
      }
    })
    .catch((error) => {
      console.error("Fetch error:", error);
      displayError("Erreur lors de la récupération du FOV.");
    });
}

// Fonction pour afficher les messages d'erreur
function displayError(message) {
  let errorMessage = document.querySelector("#errorMessage");
  errorMessage.textContent = message;
  errorMessage.style.display = "block";
}

// Fonction pour effacer les messages d'erreur
function clearError() {
  let errorMessage = document.querySelector("#errorMessage");
  errorMessage.textContent = "";
  errorMessage.style.display = "none";
}

document.addEventListener("DOMContentLoaded", () => {
  const equipmentDiv = document.getElementById("Equipment");
  const searchBtn = document.querySelector(".search-target-btn");

  if (equipmentDiv) {
    loadEquipment(equipmentDiv);
  }

  if (searchBtn) {
    searchBtn.addEventListener("click", searchTarget);
  }
});

async function loadEquipment(equipmentDiv) {
  try {
    const equipmentUrl = equipmentDiv.getAttribute("data-url-equipment");
    const data = await fetchData(equipmentUrl);
    updateSelectOptions("telescopes", data.telescopes);
    updateSelectOptions("cameras", data.cameras);
  } catch (error) {
    console.error("Erreur lors du chargement de l'équipement :", error);
  }
}

async function fetchData(url) {
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  });
  if (!response.ok) {
    throw new Error(
      `Erreur réseau: ${response.status} - ${response.statusText}`
    );
  }
  return response.json();
}

// Fonction pour mettre à jour les options des sélecteurs
function updateSelectOptions(selectId, items) {
  const select = document.getElementById(selectId);

  const optionSelectText =
    {
      telescopes: "Télescope",
      cameras: "Imageur",
    }[selectId] || "Choisir";

  select.innerHTML = `<option value="">${optionSelectText}</option>`;
  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;
    option.textContent = item.model_name;
    select.appendChild(option);
  });
}

// Fonction pour obtenir le cookie CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Événement du bouton pour sauvegarder le cadrage si l'utilisateur est satisfait
document.querySelector("#save-framing-btn").addEventListener("click", () => {
  const telescopeId = document.querySelector("#telescopes").value;
  const cameraId = document.querySelector("#cameras").value;
  const fovWidth = parseFloat(document.querySelector("#fov-width").value);
  const fovHeight = parseFloat(document.querySelector("#fov-height").value);

  const stellarObject = {
    name: document.querySelector("#stellar-name").value,
    catalog_name: document.querySelector("#catalog-name").value,
    right_ascension: parseFloat(document.querySelector("#ra").value),
    declination: parseFloat(document.querySelector("#dec").value),
    constellation: document.querySelector("#constellation").value,
    meridien: document.querySelector("#meridien").value,
  };

  saveFraming(telescopeId, cameraId, fovWidth, fovHeight, stellarObject);
});

// Fonction pour sauvegarder le cadrage
function saveFraming(
  telescopeId,
  cameraId,
  fovWidth,
  fovHeight,
  stellarObject
) {
  const url = "/enregistrer-cadrage/";
  const csrftoken = getCookie("csrftoken");

  const data = {
    name: stellarObject.name,
    catalog_name: stellarObject.catalog_name,
    right_ascension: stellarObject.right_ascension,
    declination: stellarObject.declination,
    constellation: stellarObject.constellation,
    meridien: stellarObject.meridien,
    telescope: telescopeId,
    camera: cameraId,
    fov_width: fovWidth,
    fov_height: fovHeight,
  };

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    credentials: "include",
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status !== "success") {
        displayError(data.message || "Erreur lors de l'enregistrement.");
      }
    })
    .catch((error) => {
      console.error("Error saving framing and stellar object:", error);
      displayError("Erreur lors de l'enregistrement.");
    });
}
