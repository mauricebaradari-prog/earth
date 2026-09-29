function convert(coordinate) {
    let coord = Math.abs(coordinate);
    const degree = Math.floor(coord);
    coord *= 60.0;
    const minute = Math.floor((coord - (degree * 60.0)));
    coord *= 60.0;
    const second = Math.floor(((coord - (degree * 3600.0) - (minute * 60.0)) * 10000.0));
    return `${degree}/1,${minute}/1,${second}/10000`;
}
console.log(convert(34.774952));
