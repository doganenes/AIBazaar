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

function readProductsFromCsv(filePath) {
    return new Promise((resolve, reject) => {
        const products = [];
        fs.createReadStream(filePath)
            .pipe(csv())
            .on('data', (row) => {
                if (row.ProductID && row.ProductName) {
                    products.push({
                        id: row.ProductID,
                        name: row.ProductName
                    });
                }
            })
            .on('end', () => resolve(products))
            .on('error', reject);
    });
}

function parseHtmlToRecords(productId, productName, html) {
    let str;
    if (typeof html === 'string') {
        str = html;
    } else if (html && typeof html === 'object') {
        str = html.data || JSON.stringify(html);
    } else {
        str = String(html);
    }

    str = str.replace(/""/g, '"');
    const cleanStr = str.replace(/^"|"$/g, '');
    const parts = cleanStr.split(',');

    const records = [];
    for (let i = 0; i < parts.length; i += 3) {
        let date = parts[i];
        let price = parts[i + 1];

        if (date) {
            date = date.replace(/^\[?"?/, '').replace(/"?$/, '');
        }

        if (price) {
            price = price.replace(/^"*/, '').replace(/"*$/, '');
        }

        if (date && price) {
            records.push({
                productId,
                productName,
                date,
                price
            });
        }
    }

    return records;
}


async function fetchAllProducts(productInfos) {
    const allRecords = [];
    for (const product of productInfos) {
        try {
            const html = await fetchProductById(product.id);
            const records = parseHtmlToRecords(product.id, product.name, html);
            allRecords.push(...records);
            console.log(`ID ${product.id} (${product.name}) verisi alındı. ${records.length} kayıt eklendi.`);
        } catch (error) {
            console.error(`ID ${product.id} için hata:`, error);
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
                id: 'productName',
                title: 'ProductName'
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
    console.log('✅ CSV dosyası başarıyla yazıldı.');
}

(async () => {
    try {
        const productsInfo = await readProductsFromCsv('epeyProductListid.csv');

       
        const products = await fetchAllProducts(productsInfo);

        await writeProductsToCsv(products);
    } catch (error) {
        console.error('Hata:', error);
    }
})();
