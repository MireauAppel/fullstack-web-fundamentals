function filter(array, callback) {
    let newtab = [];
    for( let i = 0; i<array.length; i++){
        if (callback(array[i]) == true){
            newtab.push(array[i]);
        }
    }
    return newtab;
}

