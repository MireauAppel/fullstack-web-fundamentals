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

            // 2. Mise à jour de la galerie (Mode Carrousel)
            if(infoGallery) {
                infoGallery.innerHTML = ""; // On vide l'ancienne galerie
                
                if (galleryData && galleryData !== "None" && galleryData.trim() !== "") {
                    const imageArray = galleryData.split(','); 
                    
                   // --- CRÉATION DU CARROUSEL ---
                    const carouselContainer = document.createElement('div');
                    carouselContainer.className = 'carousel-container';
                    
                    // NOUVEAUX STYLES : Taille parfaite et centrée
                    carouselContainer.style.height = '450px'; // Une belle hauteur
                    carouselContainer.style.width = '90%';    // Prend 90% du panneau (un peu plus petit)
                    carouselContainer.style.maxWidth = '700px'; // Ne dépasse jamais cette taille
                    carouselContainer.style.margin = '20px auto'; // Centre parfaitement la boîte
                    carouselContainer.style.borderRadius = '15px'; // Bords arrondis
                    let slides = [];
                    let currentSlideIndex = 0;

                    // On crée toutes les images
                    imageArray.forEach((imgName, index) => {
                        let imgElement = document.createElement('img');
                        imgElement.src = "/static/" + imgName.trim(); 
                        imgElement.className = 'carousel-slide';
                        
                        // La première image est active par défaut
                        if (index === 0) imgElement.classList.add('active'); 
                        
                        slides.push(imgElement);
                        carouselContainer.appendChild(imgElement);
                    });

                    // S'il y a plus d'une image, on ajoute les flèches de navigation
                    if (slides.length > 1) {
                        const prevBtn = document.createElement('button');
                        prevBtn.className = 'carousel-btn prev';
                        prevBtn.innerHTML = '&#10094;';
                        // On réduit un peu la taille des boutons pour ce petit panneau
                        prevBtn.style.padding = '8px 14px'; 
                        prevBtn.style.fontSize = '1.2rem';
                        
                        const nextBtn = document.createElement('button');
                        nextBtn.className = 'carousel-btn next';
                        nextBtn.innerHTML = '&#10095;';
                        nextBtn.style.padding = '8px 14px';
                        nextBtn.style.fontSize = '1.2rem';

                        // Logique de défilement intégrée
                        const changeSlide = (step) => {
                            slides[currentSlideIndex].classList.remove('active');
                            // Mathématique astucieuse pour boucler (ex: passer de la dernière à la première)
                            currentSlideIndex = (currentSlideIndex + step + slides.length) % slides.length;
                            slides[currentSlideIndex].classList.add('active');
                        };

                        // Empêche le clic de faire sauter la page (preventDefault)
                        prevBtn.addEventListener('click', (e) => { e.preventDefault(); changeSlide(-1); });
                        nextBtn.addEventListener('click', (e) => { e.preventDefault(); changeSlide(1); });

                        carouselContainer.appendChild(prevBtn);
                        carouselContainer.appendChild(nextBtn);
                    }

                    // On injecte le tout dans la page
                    infoGallery.appendChild(carouselContainer);
                    // --- FIN DU CARROUSEL ---

                } else {
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