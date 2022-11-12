// Chart Doughnut
var ctxDoughnut = document.getElementById('chart-doughnut').getContext("2d");

var pctg = {
  id: "pctg",
  beforeDraw(chart, args, options) {
    const { ctx, chartArea: {top, right, bottom, left, width, height} } = chart;
    ctx.save();

    ctx.font = "1.5rem sans-serif";
    ctx.fillStyle = "#1F2E23";
    ctx.textAlign = "center";
    ctx.fillText("58%", width / 2, top + (height/2) + 8);
  }
};

var donutConfig = {
  type: 'doughnut',
  data: {
    labels: ["Dostępne", "Użyte"],
    datasets: [
      {
        data: [58, 42],
        borderColor: "transparent",
        backgroundColor: [
          "#46644F",
          "#D3DCD6"
        ],
        hoverBackgroundColor: [
          "#46644F",
          "#D3DCD6"
        ]
      }]
  },
  options: {
    elements: {
      center: {
        text: '58%',
        color: '#FF6384', // Default is #000000
        fontStyle: 'Arial', // Default is Arial
        sidePadding: 20, // Default is 20 (as a percentage)
        minFontSize: 25, // Default is 20 (in px), set to false and text will not wrap.
        lineHeight: 25 // Default is 25 (in px), used for when text wraps
      }
    },
    responsive: true,
    plugins: {
      legend: {
        display: false,
      },
    },
    cutout: "60%"
  },
  plugins: [pctg]
};

var chartDoughnut = new Chart(ctxDoughnut, donutConfig);


// Chart Line

var ctxLine = document.getElementById("chart-line").getContext("2d");

var gradientStroke = ctxLine.createLinearGradient(0, 230, 0, 50);
gradientStroke.addColorStop(1, 'rgba(70,100,79,0.2)');
gradientStroke.addColorStop(0, 'rgba(70,100,79,0.0)');

var dataChartMain = {
  labels: ["Pn", "Wt", "Śr", "Cz", "Pt", "Sb", "Nd"],
  datasets: [
    {
      label: "Wydatki",
      tension: 0.4,
      borderWidth: 0,
      pointRadius: 0,
      borderColor: "#46644F",
      borderWidth: 4,
      backgroundColor: gradientStroke,
      fill: true,
      data: [150, 430, 300, 520, 350],
      maxBarThickness: 6
    }
  ],
};

var chartLine = new Chart(ctxLine, {
  type: "line",
  data: dataChartMain,
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
      }
    },
    interaction: {
      intersect: false,
      mode: 'index',
    },
    scales: {
      y: {
        grid: {
          drawBorder: false,
          display: true,
          drawOnChartArea: true,
          drawTicks: false,
          borderDash: [2, 25]
        },
        ticks: {
          display: true,
          maxTicksLimit: 5,
          color: '#b2b9bf',
          font: {
            size: 10,
            family: "Inter",
            style: 'normal',
            lineHeight: 2
          },
        },

      },
      x: {
        grid: {
          drawBorder: false,
          display: false,
          drawOnChartArea: false,
          drawTicks: false,
        },
        ticks: {
          display: true,
          color: '#b2b9bf',
          font: {
            size: 10,
            family: "Inter",
            style: 'normal',
            lineHeight: 2
          },
        }
      },
    },
  },
});