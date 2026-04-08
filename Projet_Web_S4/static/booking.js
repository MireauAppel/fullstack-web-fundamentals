document.addEventListener('DOMContentLoaded', function() {
    const startInput = document.getElementById('start_date');
    const endInput = document.getElementById('end_date');

    if (startInput && endInput) {
        // Bloquer les dates dans le passé
        const today = new Date().toISOString().split('T')[0];
        startInput.setAttribute('min', today);
        endInput.setAttribute('min', today);

        // Écouter le changement de date d'arrivée
        startInput.addEventListener('change', function() {
            endInput.setAttribute('min', this.value);
            
            if (endInput.value < this.value) {
                endInput.value = "";
            }
        });
    }
});