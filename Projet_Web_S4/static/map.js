document.addEventListener("DOMContentLoaded", function() {
    const markers = document.querySelectorAll('.map-marker');
    const infoTitle = document.querySelector('#info-panel h3');
    const infoDesc = document.getElementById('info-desc');
    const infoPrice = document.getElementById('info-price');
    const infoCapacity = document.getElementById('info-capacity');
    const infoLink = document.getElementById('info-link');
    const infoGallery = document.getElementById('info-gallery'); 

    markers.forEach(marker => {
        marker.addEventListener('click', function() {
            const name = this.getAttribute('data-name');
            const desc = this.getAttribute('data-desc');
            const price = this.getAttribute('data-price');
            const capacity = this.getAttribute('data-capacity');
            const id = this.getAttribute('data-id');
            const galleryData = this.getAttribute('data-gallery');

            // MàJ des champs texte
            if(infoTitle) infoTitle.textContent = name;
            if(infoDesc) infoDesc.textContent = desc;
            if(infoPrice) infoPrice.innerHTML = "<strong>Tarif :</strong> " + price + " € / nuit";
            if(infoCapacity) infoCapacity.innerHTML = "<strong>Capacité :</strong> " + capacity + " personnes";

            // MàJ de la galerie (Carrousel)
            if(infoGallery) {
                infoGallery.innerHTML = ""; 
                
                if (galleryData && galleryData.trim() !== "" && galleryData !== "None") {
                    const imageArray = galleryData.split(','); 
                    
                    const carouselContainer = document.createElement('div');
                    carouselContainer.className = 'carousel-container';
                    carouselContainer.style.height = '450px'; 
                    carouselContainer.style.width = '90%';   
                    carouselContainer.style.maxWidth = '700px'; 
                    carouselContainer.style.margin = '20px auto';
                    carouselContainer.style.borderRadius = '15px';
                    
                    let slides = [];
                    let currentSlideIndex = 0;

                    imageArray.forEach((imgName, index) => {
                        let imgElement = document.createElement('img');
                        imgElement.src = "/static/" + imgName.trim(); 
                        imgElement.className = 'carousel-slide';
                        
                        if (index === 0) imgElement.classList.add('active'); 
                        
                        slides.push(imgElement);
                        carouselContainer.appendChild(imgElement);
                    });

                    // Contrôles de navigation
                    if (slides.length > 1) {
                        const prevBtn = document.createElement('button');
                        prevBtn.className = 'carousel-btn prev';
                        prevBtn.innerHTML = '&#10094;';
                        prevBtn.style.padding = '8px 14px'; 
                        prevBtn.style.fontSize = '1.2rem';
                        
                        const nextBtn = document.createElement('button');
                        nextBtn.className = 'carousel-btn next';
                        nextBtn.innerHTML = '&#10095;';
                        nextBtn.style.padding = '8px 14px';
                        nextBtn.style.fontSize = '1.2rem';

                        const changeSlide = (step) => {
                            slides[currentSlideIndex].classList.remove('active');
                            currentSlideIndex = (currentSlideIndex + step + slides.length) % slides.length;
                            slides[currentSlideIndex].classList.add('active');
                        };

                        prevBtn.addEventListener('click', (e) => { e.preventDefault(); changeSlide(-1); });
                        nextBtn.addEventListener('click', (e) => { e.preventDefault(); changeSlide(1); });

                        carouselContainer.appendChild(prevBtn);
                        carouselContainer.appendChild(nextBtn);
                    }

                    infoGallery.appendChild(carouselContainer);
                } else {
                    infoGallery.innerHTML = "<p style='font-size: 0.85rem; color: #888; font-style: italic;'>Aucune photo supplémentaire disponible.</p>";
                }
            }

            // MàJ du lien de réservation
            if(infoLink) {
                infoLink.href = "/accommodation/" + id;
                infoLink.style.display = "inline-block";
            }
        });
    });
});