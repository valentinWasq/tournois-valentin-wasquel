const ctx = document.getElementById('BarGoalMatch');
new Chart(ctx, {
  type: 'bar',
  data: {
    labels: JSON.parse(ctx.getAttribute("labels").replaceAll("'",'"')),
    datasets: [{
      label: 'Buts',
      data: JSON.parse(ctx.getAttribute("data1")),
      borderWidth: 1
    },{
      label: 'Encaissés',
      data: JSON.parse(ctx.getAttribute("data2")),
      borderWidth: 1
    }],
  },

  options: {
    scales: {
      x:{
        stacked:true
      },
      y: {
        stacked:true
      }
    }
  }
});

const ctx3 = document.getElementById('GoalsTeam2');

new Chart(ctx3, {
  type: 'bubble',
  data: {
    labels: JSON.parse(ctx3.getAttribute("labels").replaceAll("'",'"')),
    datasets: [{
      label: "Buts/Encaissés",
      data: JSON.parse(ctx3.getAttribute("data").replaceAll("'",'"')),
      borderWidth: 1
    }]
  },

  options: {
    scales:  {
      x: {
        type: 'linear',
        position: 'bottom'
      }
    }
  }
});

const ctx2 = document.getElementById('GoalsTeam');

new Chart(ctx2, {
  type: 'doughnut',
  data:{
    labels:  JSON.parse(ctx2.getAttribute("labels").replaceAll("'",'"')),
    datasets: [{
      label:"Goals",
      data:  JSON.parse(ctx2.getAttribute("data")),
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(224,224, 224)',
        'rgb(153, 255, 153)',
      ],
      hoverOffset: 4
    }]
  },

  options: {

  }
});


const ctx4 = document.getElementById('PointsTeam');

new Chart(ctx4, {
  type: 'polarArea',
  data:{
    labels:  JSON.parse(ctx4.getAttribute("labels").replaceAll("'",'"')),
    datasets: [{
      label: "Points",
      data:  JSON.parse(ctx4.getAttribute("data")),
      backgroundColor: [
        'rgb(255, 99, 132)',
        'rgb(54, 162, 235)',
        'rgb(255, 205, 86)',
        'rgb(224,224, 224)',
        'rgb(153, 255, 153)',
      ],
      hoverOffset: 4
    }]
  },

  options: {

  }
});

