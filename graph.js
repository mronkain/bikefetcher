var fetchedSeries = [];
var days = 3;

var maekChart = function(date, data, legend) {
  fetchedSeries.push({name: legend[0].toUpperCase() + legend.slice(1), data: data});

  if (fetchedSeries.length == days +1) {
    fetchedSeries.sort(function(a,b) {
      return a["name"] > b["name"];
    })

    var chart = new Chartist.Line('.chart', {
      series: fetchedSeries
    }, {
      showPoint: false,
      axisY: {
        onlyInteger: true,
        low: 0
      },
      axisX: {
        type: Chartist.FixedScaleAxis,
        // change these if you want to show dates sequentially
        low: Number(new Date('2006-06-06 00:00')),
        high: Number(new Date('2006-06-07 00:00')),
        divisor: 12,
        labelInterpolationFnc: function(value) {
          return moment(value).format('HH:mm');
        }
      },
      plugins: [
        Chartist.plugins.legend()
      ]
    });
  }
}

var fetchAndDraw = function(place, date, legend) {
  fetch("https://flexer.430am.fi/salmisaari_history/" + place + "_" + date + ".tsv").then(function(response) {
    return response.text();
  }).then(function(text) {
    var arr = text.split("\n");
    var dataset = [];
    for (var i in arr) {
      line = arr[i].split("\t");
      // use date from line[0] to show days sequentially
      dataset.push({x: new Date("2006-06-06" + " " + line[1]), y: line[2]})
    }
    maekChart(date, dataset, legend);
  }).catch(function(error) {
    maekChart(date, [], "-")
});
}

var place = "both";

var url = new URL(window.location);
var p = url.searchParams.get("place");

if (p == "porkkala") {
  place = "porkkala";
  el = document.getElementById("place");
  el.selectedIndex = 2;
} else if (p == "salmisaari") {
  place = "salmisaari";
  el = document.getElementById("place");
  el.selectedIndex = 1;  
} 

if (place != "both") {
  fetchAndDraw(place, moment().format("YYYY-MM-DD"), "today (" + moment().format("dd") + ")");
  for (var i = 1; i <= days; i++) {
    fetchAndDraw(place, moment().subtract(i, 'days').format("YYYY-MM-DD"),  "yester".repeat(i) + "day (" + moment().subtract(i, 'days').format("dd") + ")");
  }
} else {
  days = 1;
  fetchAndDraw("porkkala", moment().format("YYYY-MM-DD"), "Porkkalankatu");
  fetchAndDraw("salmisaari", moment().format("YYYY-MM-DD"), "Salmiraarenranta");
}