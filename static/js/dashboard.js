'use strict'

let testChart 
const selectExercise = document.querySelectorAll('.dropdown-item')
for (const button of selectExercise) 
  button.addEventListener('click', event => {
    console.log(event)
    const exercise_id = button.id;
    fetch('/chart_data', {
      method: 'POST',
      body: JSON.stringify({"exercise_id": exercise_id}),
      headers: {
        'Content-Type': 'application/json'
      },
    }).then(response=> response.json())
      .then((responseJson) => {
        const dataForChart = responseJson;
        const labels = []
        const data = []
        for (const key in dataForChart ) {
          labels.push(key);
          data.push(dataForChart[key])
        }
        if (testChart){
          testChart.destroy()
        };
        testChart = new Chart(
          document.querySelector('#test-chart'),
          {
            type: 'line',
            data: {
              labels: labels,
              datasets: [
                { label: 'lb(s)',
                  data: data}
              ]},
            options: {
              plugins: {
                title: {
                  display: true,
                  text: "Strength Progression Over Time"
                }
              }
            }
          }
        );
        console.log(responseJson);
        return responseJson;
      }
      )
})