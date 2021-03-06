//========================================================================
// Constants
///=======================================================================
const COLORS = ['#ff6347', '#ffd700', '#65d26e', '#87ceeb', '#ffffff'];

// jQuery
//var geocode = JSON.parse($("#polar").data("blind"));
//alert(geocode);


setTimeout("alert('Boom!');", 50000);
// Parse our data to JSON
var artist = JSON.parse(artistData);
alert(artist['albums'][0]['name']);

Chart.defaults.global.responsive = false;
Chart.defaults.global.animation.duration = 500;
Chart.defaults.global.hover.mode = 'nearest';
Chart.defaults.global.datasets.line = {
    showLine: true,
    fill: false,
    borderWidth: 2,
    pointRadius: 2,
    pointHitRadius: 8,
};
Chart.defaults.global.legend = {
    ...(Chart.defaults.global.legend),
    position: 'bottom',
    align: 'start',
};
Chart.defaults.global.legend.labels = {
    ...(Chart.defaults.global.legend.labels),
    boxWidth: 6,
    fontSize: 14,
    fontColor: '#bbbbbb',
    padding: 32,
    usePointStyle: true,
};
Chart.defaults.global.defaultFontSize = 14;
Chart.defaults.scale.gridLines = {
    ...(Chart.defaults.scale.gridLines),
    display: true, 
    color: 'transparent', 
    zeroLineColor: "#606060"
};
Chart.defaults.scale.scaleLabel = {
    ...(Chart.defaults.scale.scaleLabel),
    display: false,
    fontColor: "#bbbbbb",
};
Chart.defaults.scale.ticks.fontColor = '#606060';

// Get all the songs and push them into array where all songs will recide.
var i;
var allSongs = []
var j;
for(i = 0; i < artist['albums'].length; i++) {
  var album = artist['albums'][i]['songs']; //const labels = artist['albums'].map((a, i) => a.songs.map(s => s.name))
  for(j = 0; j < album.length; j++) {
    allSongs.push(album[j]['name'])
  }
  
}

const datasets = artist['albums'].map((album, i) => {
  // For each song in the album get the label (name of song), the starting x point and it's y point.
  // In addition, get the valence and polarity values. The points variable returns an array with the values.
  const points = album.songs.map((s, j) => ({
      label: s.name,
      x: j + 1,
      y: (((s.valence * 2) - 1) * 0.7) + (s.polarity) * 0.3,
      valence: (s.valence * 2) - 1,
      polarity: s.polarity
  }));
  const color = COLORS[i % COLORS.length];

  // The dataset variable returns an array with the values listed below.
  return {
      defaultColor: color,
      borderColor: color + '55', // line
      backgroundColor: color, // inside points/legends
      pointBorderColor: color, // points/legends ring
      label: album.name,
      data: points
  }
});



var ctx = document.getElementById("myChart");

var myChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: allSongs,
    datasets: datasets
  },
  options: {
    legend: {
      onHover: (e, _) => e.target.style.cursor = 'pointer',
      onLeave: (e, _) => e.target.style.cursor = 'default',
    },
    scales: {
      xAxes: [{
          type: 'linear',
          scaleLabel: { labelString: 'Valence' },
          ticks: {
              display: false,
              stepSize: 1,
              suggestedMin: 0,
              suggestedMax: Math.max(...datasets.map(d => d.data.length)) + 1,
          },
      }],
      yAxes: [{
          scaleLabel: { labelString: 'Polarity' },
          ticks: {
              padding: 10, 
              min: -1.2, 
              max: 1.2,
              callback: (val, i, values) => {
                  return {
                      '-1': 'Dark (-1)',
                      '0': 'Neutral (0)',
                      '1': 'Positive (1)',
                  }[val] || '';
              }
          }
      }]
  },
  tooltips: {
    callbacks: {
        title: function(items, data) {
            const { datasetIndex, index } = items[0];
            const dataset = data.datasets[datasetIndex];
            let label = dataset.data[index].label || '';
            myChart.update();
            return label;
        },
        label: function(item, data) {
            const dataset = data.datasets[item.datasetIndex];
            const { valence, polarity } = dataset.data[item.index];
            const _valence = valence.toFixed(3);
            const _polarity = polarity.toFixed(3);
            myChart.update();
            return `(${_valence}, ${_polarity})`;
        }
    }
}
  }
});