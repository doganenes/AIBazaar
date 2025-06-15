export const createChartData = (forecastData, todayDate, addDaysToDate) => {
  return {
    labels: forecastData.map((_, index) => addDaysToDate(todayDate, index)),
    datasets: [
      {
        label: "Estimated price (₺)",
        data: forecastData,
        borderColor: "rgb(59, 130, 246)",
        backgroundColor: "rgba(59, 130, 246, 0.1)",
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: "rgb(59, 130, 246)",
        pointBorderColor: "#fff",
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        pointHoverBackgroundColor: "rgb(37, 99, 235)",
      },
    ],
  };
};

export const createChartOptions = () => {
  return {
    responsive: true,
    maintainAspectRatio: false,
    animation: {
      duration: 1000,
      easing: "easeInOutQuart",
    },
    interaction: {
      intersect: false,
      mode: "index",
    },
    scales: {
      y: {
        beginAtZero: false,
        grid: {
          color: "rgba(0, 0, 0, 0.1)",
        },
        ticks: {
          callback: function (value) {
            return new Intl.NumberFormat("tr-TR", {
              style: "currency",
              currency: "TRY",
              minimumFractionDigits: 0,
            }).format(value);
          },
        },
      },
      x: {
        grid: {
          color: "rgba(0, 0, 0, 0.1)",
        },
      },
    },
    plugins: {
      tooltip: {
        backgroundColor: "rgba(0, 0, 0, 0.8)",
        titleColor: "#fff",
        bodyColor: "#fff",
        borderColor: "rgb(59, 130, 246)",
        borderWidth: 1,
        cornerRadius: 8,
        callbacks: {
          label: function (context) {
            return `Estimated Price: ${new Intl.NumberFormat("tr-TR", {
              style: "currency",
              currency: "TRY",
            }).format(context.parsed.y)}`;
          },
        },
      },
      legend: {
        display: false,
      },
    },
  };
};

export const calculateStats = (forecastData) => {
  if (!forecastData.length) return null;

  const min = Math.min(...forecastData);
  const max = Math.max(...forecastData);
  const avg = forecastData.reduce((a, b) => a + b, 0) / forecastData.length;
  const trend = forecastData[forecastData.length - 1] - forecastData[0];
  const trendPercent = ((trend / forecastData[0]) * 100).toFixed(1);

  return { min, max, avg, trend, trendPercent };
};