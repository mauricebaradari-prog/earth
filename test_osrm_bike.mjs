const wp1 = "32.6289967,34.6657239"; // Petra
const wp2 = "32.6962141,34.674622"; // Pissouri

async function test(profile) {
    const url = `https://router.project-osrm.org/route/v1/${profile}/${wp1};${wp2}?overview=false`;
    try {
        const res = await fetch(url);
        const data = await res.json();
        const dist = (data.routes[0].distance / 1000).toFixed(1);
        console.log(`${profile}: ${dist} km`);
    } catch(e) { console.log(profile, 'error'); }
}

test('driving');
test('bike');
test('foot');
