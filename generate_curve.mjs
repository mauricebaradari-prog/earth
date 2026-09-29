function getCurvePoints(p1, p2, control, numPoints) {
    const pts = [];
    for (let i = 0; i <= numPoints; i++) {
        const t = i / numPoints;
        const lat = (1-t)*(1-t)*p1.lat + 2*(1-t)*t*control.lat + t*t*p2.lat;
        const lng = (1-t)*(1-t)*p1.lng + 2*(1-t)*t*control.lng + t*t*p2.lng;
        pts.push({ lat, lng });
    }
    return pts;
}
const petra = { lat: 34.6657239, lng: 32.6289967 };
const pissouri = { lat: 34.674622, lng: 32.6962141 };
// Control point south of both, to make it bow out over the coast
const control = { lat: 34.640, lng: 32.660 };

const curve = getCurvePoints(petra, pissouri, control, 15);
curve.forEach((p, i) => {
    console.log(`      { id: 'wp9-coast-${i}', name: 'Coast', country: 'Cyprus', lat: ${p.lat.toFixed(5)}, lng: ${p.lng.toFixed(5)} },`);
});
