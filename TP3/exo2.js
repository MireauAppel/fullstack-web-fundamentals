function filter(array, callback) {
    let newtab = [];
    for( let i = 0; i<array.length; i++){
        if (callback(array[i]) == true){
            newtab.push(array[i]);
        }
    }
    return newtab;
}

let mots=["LEAGUE", "data", "RIOT", "insight", "Analyst"]
function pas_maj(chaine){
    return chaine != chaine.toUpperCase();
}

let mots_filtres = filter(mots, pas_maj);
console.log(mots_filtres);