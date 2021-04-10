
(function ($) {
  "use strict";

  try {
    var ctx = document.getElementById("widgetChart1");
    if (ctx) {
      ctx.height = 100;
      var myChart = new Chart(ctx, {
        type: 'line',
        data: {
          type: 'line'

        },
        options: {
          maintainAspectRatio: true,
          legend: {
            display: false
          },
          layout: {
            padding: {
              left: 0,
              right: 0,
              top: 0,
              bottom: 0
            }
          },
          responsive: true,
          scales: {
            xAxes: [{
              gridLines: {
                color: 'transparent',
                zeroLineColor: 'transparent'
              },
              ticks: {
                fontSize: 2,
                fontColor: 'transparent'
              }
            }],
            yAxes: [{
              display: false,
              ticks: {
                display: false,
              }
            }]
          },
          title: {
            display: false,
          },
          elements: {
            line: {
              borderWidth: 0
            },
            point: {
              radius: 0,
              hitRadius: 10,
              hoverRadius: 4
            }
          }
        }
      });
    }

    var ctx = document.getElementById("percent-chart");
    if (ctx) {
      ctx.height = 200;
      var myChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
          datasets: [
            {
              backgroundColor: [
                '#00b5e9',
                '#fa4251'
              ],
              hoverBackgroundColor: [
                '#00b5e9',
                '#fa4251'
              ],
              borderWidth: [
                0, 0
              ],
              hoverBorderColor: [
                'transparent',
                'transparent'
              ]
            }
          ]
        },
        options: {
          maintainAspectRatio: false,
          responsive: true,
          cutoutPercentage: 55,
          animation: {
            animateScale: true,
            animateRotate: true
          },
          legend: {
            display: false
          },
          tooltips: {
            titleFontFamily: "Poppins",
            xPadding: 15,
            yPadding: 10,
            caretPadding: 0,
            bodyFontSize: 16
          }
        }
      });
    }

  } catch (error) {
    console.log(error);
  }

  var text = "{{stServico}}".replaceAll("&#34;", '"').replaceAll('"label"',"label").replaceAll('"data"',"data").replaceAll('"borderColor"',"borderColor").replaceAll('"borderWidth"',"borderWidth").replaceAll('"backgroundColor"',"backgroundColor").replaceAll('"fontFamily"',"fontFamily").replaceAll('"(_',"[").replaceAll('_)"',"]");
  try {
    var ctx = document.getElementById("barChart");
    if (ctx) {
      ctx.height = 100;
      var myChart = new Chart(ctx, {
        type: 'bar',
        defaultFontFamily: 'Poppins',
        data: {
          labels: ["Alvenaria", "Forro de Gesso", "Elétrica", "Hidráulica", "Revestimento", "Pintura", "Acabamentos", "Ar Condicionado"],
          datasets: [
            {
              label: "Fases",
              data: [65, 59, 80, 81, 56, 55, 40, 80],
              borderColor: "rgba(0, 123, 255, 0.9)",
              borderWidth: "0",
              backgroundColor: "rgba(0, 123, 255, 0.5)",
              fontFamily: "Poppins"
            },
          ]
        },
        options: {
          legend: {
            position: 'top',
            labels: {
              fontFamily: 'Poppins'
            }

          },
          scales: {
            xAxes: [{
              ticks: {
                fontFamily: "Poppins"

              }
            }],
            yAxes: [{
              ticks: {
                beginAtZero: true,
                fontFamily: "Poppins"
              }
            }]
          }
        }
      });
    }


  } catch (error) {
    console.log(error);
  }
 
})(jQuery);



