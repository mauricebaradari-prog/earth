const wp1 = "32.6289967,34.6657239"; // Petra
const wp2 = "32.6962141,34.674622"; // Pissouri

async function test(label, wps) {
    const url = `https://router.project-osrm.org/route/v1/driving/${wp1};${wps};${wp2}?overview=false`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        const dist = (data.routes[0].distance / 1000).toFixed(1);
        console.log(`${label}: ${dist} km`);
    } catch(e) { console.log(label, 'error'); }
}

test('B6-1', "32.6524475,34.6607716");
test('B6-2', "32.6851291,34.6727244");
test('Both', "32.6524475,34.6607716;32.6851291,34.6727244");
