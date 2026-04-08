document.addEventListener("DOMContentLoaded", function() {
    const markers = document.querySelectorAll('.map-marker');
    const infoTitle = document.querySelector('#info-panel h3');
    const infoDesc = document.getElementById('info-desc');
    const infoPrice = document.getElementById('info-price');
    const infoLink = document.getElementById('info-link');
    const infoGallery = document.getElementById('info-gallery'); // NOUVEAU

    markers.forEach(marker => {
        marker.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const desc = this.getAttribute('data-desc');
            const price = this.getAttribute('data-price');
            const id = this.getAttribute('data-id');
            const images = this.getAttribute('data-images'); // NOUVEAU

            infoTitle.textContent = name;
            infoDesc.textContent = desc;
            infoPrice.innerHTML = "<strong>Tarif :</strong> " + price + " € / nuit";

            // GESTION DE LA GALERIE D'IMAGES
            infoGallery.innerHTML = ""; // On vide l'ancienne galerie
            if (images) {
                // On découpe la chaîne "vue1.jpg,vue2.jpg" en un vrai tableau
                const imageArray = images.split(','); 
                
                imageArray.forEach(imgName => {
                    // Pour chaque image, on crée une balise <img>
                    let imgElement = document.createElement('img');
                    // On construit le lien vers le dossier static
                    imgElement.src = "/static/" + imgName.trim(); 
                    infoGallery.appendChild(imgElement);
                });
            }

            infoLink.href = "/accommodation/" + id;
            infoLink.style.display = "inline-block";
        });
    });
});