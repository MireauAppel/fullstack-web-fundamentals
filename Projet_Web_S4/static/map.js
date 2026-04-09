document.addEventListener("DOMContentLoaded", function() {
    const markers = document.querySelectorAll('.map-marker');
    const infoTitle = document.querySelector('#info-panel h3');
    const infoDesc = document.getElementById('info-desc');
    const infoPrice = document.getElementById('info-price');
    const infoLink = document.getElementById('info-link');
    const infoGallery = document.getElementById('info-gallery'); 

    markers.forEach(marker => {
        marker.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const desc = this.getAttribute('data-desc');
            const price = this.getAttribute('data-price');
            const id = this.getAttribute('data-id');
            const galleryData = this.getAttribute('data-gallery');

            // 1. Mise à jour des textes
            if(infoTitle) infoTitle.textContent = name;
            if(infoDesc) infoDesc.textContent = desc;
            if(infoPrice) infoPrice.innerHTML = "<strong>Tarif :</strong> " + price + " € / nuit";

            // 2. Mise à jour de la galerie (avec sécurité)
            if(infoGallery) {
                infoGallery.innerHTML = ""; // On vide l'ancienne galerie
                
                // On vérifie que galleryData existe et n'est pas vide
                if (galleryData && galleryData !== "None" && galleryData.trim() !== "") {
                    const imageArray = galleryData.split(','); 
                    
                    imageArray.forEach(imgName => {
                        let imgElement = document.createElement('img');
                        // .trim() est crucial pour enlever les espaces après les virgules
                        imgElement.src = "/static/" + imgName.trim(); 
                        infoGallery.appendChild(imgElement);
                    });
                } else {
                    // Message de secours si aucune image n'est trouvée
                    infoGallery.innerHTML = "<p style='font-size: 0.85rem; color: #888; font-style: italic;'>Aucune photo supplémentaire disponible.</p>";
                }
            }

            // 3. Mise à jour du bouton
            if(infoLink) {
                infoLink.href = "/accommodation/" + id;
                infoLink.style.display = "inline-block";
            }
        });
    });
});
