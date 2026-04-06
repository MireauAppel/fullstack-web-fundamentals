document.addEventListener("DOMContentLoaded", function() {
    // 1. On récupère toutes les maisons de la carte
    const markers = document.querySelectorAll('.map-marker');
    
    // 2. On récupère les éléments du panneau d'information à mettre à jour
    const infoTitle = document.querySelector('#info-panel h3');
    const infoDesc = document.getElementById('info-desc');
    const infoPrice = document.getElementById('info-price');
    const infoLink = document.getElementById('info-link');

    // 3. Pour chaque maison, on ajoute un "écouteur de clic"
    markers.forEach(marker => {
        marker.addEventListener('click', function() {
            // On lit les données cachées dans le HTML (data-...)
            const name = this.getAttribute('data-name');
            const desc = this.getAttribute('data-desc');
            const price = this.getAttribute('data-price');
            const id = this.getAttribute('data-id');

            // On met à jour le texte du panneau (manipulation du DOM)
            infoTitle.textContent = name;
            infoDesc.textContent = desc;
            infoPrice.innerHTML = "<strong>Tarif :</strong> " + price + " € / nuit";

            // On met à jour le lien du bouton et on l'affiche
            infoLink.href = "/accommodation/" + id;
            infoLink.style.display = "inline-block";
        });
    });
});