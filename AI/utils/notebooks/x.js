const url = 'https://www.epey.com/kat/fg/';
const payload = new URLSearchParams({
    id: '902114'

});

fetch(url, {
    method: 'POST',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'application/json, */*; q=0.01',
        'Referer': 'https://www.epey.com/kat/fg/',
        'Origin': 'https://www.epey.com',
    },
    body: payload.toString()
})
.then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json(); 
})
.then(html => {
    console.log('Gelen HTML:', html);
    // DOMParser ile HTML parçalayabilirsin:
    
})
.catch(error => {
    console.error('İstek hatası:', error);
});
