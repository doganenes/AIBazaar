const fs = require('fs');
const csv = require('csv-parser');
const {
    URLSearchParams
} = require('url');
const createCsvWriter = require('csv-writer').createObjectCsvWriter;

async function fetchProductById(id) {
    const url = 'https://www.epey.com/kat/fg/';
    const payload = new URLSearchParams({
        id
    });

    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest',
                'Accept': 'application/json, */*; q=0.01',
                'Referer': 'https://www.epey.com/kat/fg/',
                'Origin': 'https://www.epey.com',
            },
            body: payload.toString()
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        return await response.json();
    } catch (error) {
        console.error('İstek hatası:', error);
        throw error;
    }
}

function readIdsFromCsv(filePath) {
    return new Promise((resolve, reject) => {
        const ids = [];
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (row) => {
                if (row.ProductID) ids.push(row.ProductID);
            })
            .on('end', () => resolve(ids))
            .on('error', reject);
    });
}

function parseHtmlToRecords(productId, html) {
    let str;
    if (typeof html === 'string') {
        str = html;
    } else if (html && typeof html === 'object') {
        str = html.data || JSON.stringify(html);
    } else {
        str = String(html);
    }

    // Gereksiz çift tırnakları tek tırnağa indir
    str = str.replace(/""/g, '"');

    // Başta sondaki tırnakları temizle
    const cleanStr = str.replace(/^"|"$/g, '');

    const parts = cleanStr.split(',');

    const records = [];
    for (let i = 0; i < parts.length; i += 3) {
        // date ve price değerlerini gereksiz karakterlerden temizle
        let date = parts[i];
        let price = parts[i + 1];

        if (date) {
            // date'den baştaki [ ve tırnakları kaldır
            date = date.replace(/^\[?"?/, '').replace(/"?$/, '');
        }

        if (price) {
            // price'dan baştaki tırnakları kaldır
            price = price.replace(/^"*/, '').replace(/"*$/, '');
        }

        if (date && price) {
            records.push({
                productId,
                date,
                price
            });
        }
    }

    return records;
}



async function fetchAllProducts(ids) {
    const allRecords = [];
    for (const id of ids) {
        try {
            const html = await fetchProductById(id);
            const records = parseHtmlToRecords(id, html);
            allRecords.push(...records);
            console.log(`ID ${id} verisi alındı. ${records.length} kayıt eklendi.`);
        } catch (error) {
            console.error(`ID ${id} için hata:`, error);
        }
    }
    return allRecords;
}

async function writeProductsToCsv(products) {
    const csvWriter = createCsvWriter({
        path: 'products.csv',
        header: [{
                id: 'productId',
                title: 'ProductID'
            },
            {
                id: 'date',
                title: 'Date'
            },
            {
                id: 'price',
                title: 'Price'
            }
        ]
    });

    await csvWriter.writeRecords(products);
    console.log('CSV dosyası başarıyla yazıldı.');
}

(async () => {
    try {
        const ids = await readIdsFromCsv('epeyProductListid.csv');
        console.log(`Toplam ${ids.length} ID bulundu.`);
        const products = await fetchAllProducts(ids);
        await writeProductsToCsv(products);
    } catch (error) {
        console.error('Hata:', error);
    }
})();
