let aladin;
let fovOverlay;

document.addEventListener("DOMContentLoaded", () => {
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
  });

  setupEventListeners();
  loadEquipment();
});

function fetchAladinData() {
  const proxyUrl = "/proxy-aladin/";

  fetch(proxyUrl)
  .then(response => {
    console.log("Réponse du proxy :", response);
    return response.json();
  })
  .then(data => {
    console.log("Données reçues lors de l'appel au proxy :", data);
  })
  .catch(error => console.error("Erreur de récupération des données lors de l'appel au proxy:", error));
}

// Fonction pour récupérer les données depuis une URL
async function fetchData(url) {
  const response = await fetch(url, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
    },
    credentials: "include",
  });
  if (!response.ok) {
    throw new Error(`Erreur réseau: ${response.status} - ${response.statusText}`);
  }
  return response.json();
}

async function loadEquipment() {
  try {
    const url = "equipement/";
    const data = await fetchData(url);
    updateSelectOptions("telescopes", data.telescopes);
    updateSelectOptions("cameras", data.cameras);
  } catch (error) {
    console.error("Erreur lors du chargement de l'équipement :", error);
  }
}

// Fonction pour mettre à jour les options des sélecteurs
function updateSelectOptions(selectId, items) {
  const select = document.getElementById(selectId);

  const optionSelectText =
    {
      telescopes: "Télescope",
      cameras: "Imageur",
    } [selectId] || "Choisir";

  select.innerHTML = `<option value="">${optionSelectText}</option>`;

  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item.id;

    option.textContent =
      selectId === "telescopes"
        ? `${item.model_name} ${item.aperture}/${item.focal_length}`
        : item.model_name;



    //option.textContent = `${item.model_name} (${item.aperture}/${item.focal_length})`;
    select.appendChild(option);
  });
}

function setupEventListeners() {
  document
    .querySelector(".search-target-btn")
    .addEventListener("click", searchTarget);
}

// Fonction de recherche d'un astre
async function searchTarget(event) {
  event.preventDefault();
  clearError();

  let targetName = document.getElementById("search-input").value.trim();
  let telescopeId = document.getElementById("telescopes").value;
  let cameraId = document.getElementById("cameras").value;

  if (!targetName) {
    return displayError("Veuillez entrer un nom d'astre.");
  }
  if (!telescopeId || !cameraId) {
    return displayError("Veuillez sélectionner un télescope et une caméra.");
  }

  try {
    const raDec = await gotoTarget(targetName);
    aladin.setImageSurvey("P/DSS2/color");
    
     // Si un télescope et une caméra sont sélectionnés, on récupère et affiche le FOV
     if (telescopeId && cameraId) {
      await fetchFov(telescopeId, cameraId, raDec);
    } else {
      console.log("Télescope ou imageur non sélectionné.");
    }
  } catch (error) {
    console.error("Erreur dans searchTarget :", error);
  }
}


async function gotoTarget(targetName) {
  return new Promise((resolve, reject) => {
    aladin.gotoObject(targetName, {
      success: (raDec) => {
        if (raDec) {
          console.log(`Astre ${targetName} trouvé avec succès.`);
          resolve(raDec); 
        } else {
          displayError(`Aucun résultat pour ${targetName}.`);
          reject("Aucun résultat trouvé pour l'astre.");
        }
      },
      error: () => {
        displayError(`Erreur lors de la recherche de ${targetName}.`);
        reject("Erreur lors de la recherche de l'astre.");
      },
    });
  });
}

// Fonction pour récupérer le champ de vision (FOV)
async function fetchFov(telescopeId, cameraId, raDec) {
  const url = `/calcul-fov/${telescopeId}/${cameraId}`;

  try {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
    });

    const data = await response.json();

    if (data.status === "success") {
      console.log("FOV calculé :", data);
      drawFovRectangle(data.data.fov_width, data.data.fov_height, raDec);
    } else {
      displayError("Erreur lors du calcul du champ de vision.");
    }
  } catch (error) {
    displayError("Erreur réseau lors de la récupération du FOV.");
  }
}

// Fonction pour dessiner un rectangle représentant le FOV
function drawFovRectangle(fovWidth, fovHeight, raDec) {
  fovOverlay.removeAll(); // Supprimer tous les anciens polygones

  if (!raDec) {
    return displayError("Coordonnées de l'astre non disponibles.");
  }

  const [ra, dec] = raDec;
  console.log(`Dessin du FOV autour de ${ra}, ${dec}`);

  // Calculate FOV rectangle coordinates
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
    aladin.setFoV(Math.max(fovWidth, fovHeight) * 1.5);
}

// Fonction pour effacer les messages d'erreur
function clearError() {
  document.querySelector("#searchErrorMessage").classList.add("d-none");

}

// Fonction pour afficher les messages d'erreur
function displayError(message) {
  const aladinErrorMessage = document.querySelector("#aladinErrorMessage");
  aladinErrorMessage.textContent = message;
  aladinErrorMessage.classList.remove("d-none");
}


