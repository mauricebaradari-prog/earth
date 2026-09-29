const wp1 = "32.6289967,34.6657239"; // Petra
const wp2 = "32.605,34.680"; // Aphrodite Hills
const wp3 = "32.716,34.654"; // Pissouri Bay
const wp4 = "32.6962141,34.674622"; // Pissouri

async function test(label, wps) {
    const url = `https://router.project-osrm.org/route/v1/driving/${wps}?overview=false`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        const dist = (data.routes[0].distance / 1000).toFixed(1);
        console.log(`${label}: ${dist} km`);
    } catch(e) { console.log(label, 'error'); }
}

test('Petra->Aphrodite->Bay->Pissouri', `${wp1};${wp2};${wp3};${wp4}`);
