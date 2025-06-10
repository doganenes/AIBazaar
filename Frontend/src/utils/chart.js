class MultiProductPriceChart {
    constructor(canvasId, options = {}) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        this.chart = null;
        this.rawData = [];
        this.filteredData = [];
        
        this.options = {
            maxProducts: options.maxProducts || 50,
            enableAnimation: options.enableAnimation || false,
            enableZoom: options.enableZoom !== false,
            dateFormat: options.dateFormat || 'DD.MM.YYYY',
            currency: options.currency || 'TL',
            locale: options.locale || 'tr-TR',
            colors: options.colors || this.generateColors(1000),
            ...options
        };
        
        this.initChart();
    }

    // Renk paleti oluştur
    generateColors(count) {
        const colors = [];
        for (let i = 0; i < count; i++) {
            const hue = (i * 137.508) % 360; // Golden angle
            const saturation = 60 + (i % 3) * 15;
            const lightness = 45 + (i % 4) * 10;
            colors.push(`hsl(${hue}, ${saturation}%, ${lightness}%)`);
        }
        return colors;
    }

    // Veri yükle
    loadData(data) {
        this.rawData = this.processData(data);
        this.applyFilters();
        return this;
    }

    // Veriyi işle ve normalize et
    processData(data) {
        if (!Array.isArray(data)) return [];
        
        return data.map((item, index) => {
            // Farklı veri formatlarını destekle
            if (item.productData) {
                // Format 1: { productName, productId, productData: [{date, price}] }
                return {
                    id: item.productId || `product_${index}`,
                    name: item.productName || `Ürün ${index + 1}`,
                    data: item.productData.map(d => ({
                        x: new Date(d.date),
                        y: parseFloat(d.price.toString().replace(/[^\d.-]/g, ''))
                    }))
                };
            } else if (item.data) {
                return {
                    id: item.id || `product_${index}`,
                    name: item.name || `Ürün ${index + 1}`,
                    data: item.data.map(d => ({
                        x: new Date(d.date),
                        y: parseFloat(d.price.toString().replace(/[^\d.-]/g, ''))
                    }))
                };
            } else {
                const groupedData = {};
                data.forEach(row => {
                    const key = row.productName || row.name || 'Unknown';
                    if (!groupedData[key]) {
                        groupedData[key] = [];
                    }
                    groupedData[key].push({
                        x: new Date(row.date),
                        y: parseFloat(row.price.toString().replace(/[^\d.-]/g, ''))
                    });
                });
                
                return Object.keys(groupedData).map((name, idx) => ({
                    id: `product_${idx}`,
                    name: name,
                    data: groupedData[name].sort((a, b) => a.x - b.x)
                }));
            }
        }).flat().filter(item => item.data && item.data.length > 0);
    }

    applyFilters(filters = {}) {
        let filtered = [...this.rawData];
        
        if (filters.search) {
            const searchTerm = filters.search.toLowerCase();
            filtered = filtered.filter(product => 
                product.name.toLowerCase().includes(searchTerm)
            );
        }
        
        if (filters.priceRange) {
            const [min, max] = filters.priceRange;
            filtered = filtered.filter(product => {
                const avgPrice = product.data.reduce((sum, item) => sum + item.y, 0) / product.data.length;
                return avgPrice >= min && avgPrice <= max;
            });
        }
        
        if (filters.dateRange) {
            const [startDate, endDate] = filters.dateRange.map(d => new Date(d));
            filtered = filtered.map(product => ({
                ...product,
                data: product.data.filter(item => item.x >= startDate && item.x <= endDate)
            })).filter(product => product.data.length > 0);
        }
        
        const limit = filters.limit || this.options.maxProducts;
        if (limit && limit < filtered.length) {
            filtered = filtered.slice(0, limit);
        }
        
        this.filteredData = filtered;
        this.updateChart();
        return this;
    }

    initChart() {
        Chart.defaults.font.size = 11;
        Chart.defaults.elements.point.radius = 0;
        Chart.defaults.elements.line.borderWidth = 1.5;
        Chart.defaults.animation.duration = this.options.enableAnimation ? 750 : 0;
    }

    updateChart() {
        if (this.chart) {
            this.chart.destroy();
        }

        if (!this.filteredData.length) {
            console.warn('Gösterilecek veri bulunamadı');
            return this;
        }

        const datasets = this.filteredData.map((product, index) => ({
            label: product.name,
            data: product.data,
            borderColor: this.options.colors[index % this.options.colors.length],
            backgroundColor: this.options.colors[index % this.options.colors.length] + '20',
            tension: 0.1,
            pointRadius: this.filteredData.length > 20 ? 0 : 1,
            borderWidth: this.filteredData.length > 100 ? 1 : 2,
            fill: false
        }));

        this.chart = new Chart(this.ctx, {
            type: 'line',
            data: { datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                animation: this.options.enableAnimation ? { duration: 750 } : false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            tooltipFormat: 'dd MMM yyyy',
                            displayFormats: {
                                day: 'dd MMM',
                                week: 'dd MMM',
                                month: 'MMM yyyy'
                            }
                        },
                        title: {
                            display: true,
                            text: 'Tarih'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: `Fiyat (${this.options.currency})`
                        },
                        ticks: {
                            callback: (value) => {
                                return new Intl.NumberFormat(this.options.locale).format(value);
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            title: (context) => {
                                return new Date(context[0].parsed.x).toLocaleDateString(this.options.locale);
                            },
                            label: (context) => {
                                const price = new Intl.NumberFormat(this.options.locale).format(context.parsed.y);
                                return `${context.dataset.label}: ${price} ${this.options.currency}`;
                            }
                        }
                    },
                    legend: {
                        display: this.filteredData.length <= 15,
                        position: 'top',
                        labels: {
                            usePointStyle: true,
                            pointStyle: 'line',
                            boxWidth: 20
                        }
                    },
                    zoom: this.options.enableZoom ? {
                        zoom: {
                            wheel: { enabled: true },
                            pinch: { enabled: true },
                            mode: 'xy'
                        },
                        pan: {
                            enabled: true,
                            mode: 'xy'
                        }
                    } : undefined
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });

        return this;
    }

    resetZoom() {
        if (this.chart && this.chart.resetZoom) {
            this.chart.resetZoom();
        }
        return this;
    }

    toggleAnimation() {
        this.options.enableAnimation = !this.options.enableAnimation;
        this.updateChart();
        return this;
    }

    exportCSV() {
        const header = ['Ürün Adı', 'Tarih', 'Fiyat'];
        const rows = this.filteredData.flatMap(product =>
            product.data.map(item => [
                product.name,
                item.x.toLocaleDateString(this.options.locale),
                item.y
            ])
        );
        
        const csvContent = [header, ...rows]
            .map(row => row.map(cell => `"${cell}"`).join(','))
            .join('\n');
            
        const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'urun_fiyat_analizi.csv';
        link.click();
        
        return this;
    }

    getStats() {
        const allPrices = this.filteredData.flatMap(product => 
            product.data.map(item => item.y)
        );
        
        if (!allPrices.length) return null;
        
        const minPrice = Math.min(...allPrices);
        const maxPrice = Math.max(...allPrices);
        const avgPrice = allPrices.reduce((a, b) => a + b, 0) / allPrices.length;
        
        return {
            totalProducts: this.filteredData.length,
            totalDataPoints: allPrices.length,
            minPrice,
            maxPrice,
            avgPrice,
            priceRange: maxPrice - minPrice
        };
    }

    destroy() {
        if (this.chart) {
            this.chart.destroy();
            this.chart = null;
        }
        return this;
    }
}
