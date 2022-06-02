'use strict'
// const dataForChart = {
//   "2022-05-02": 0.0,
//   "2022-05-10": 5.0,
//   "2022-05-30": 5.0
// };

// const labels = []
// const data = []
// for (const key in dataForChart ) {
//   labels.push(key);
//   data.push(dataForChart[key])
// }

// const testChart = new Chart(
//   document.querySelector('#test-chart'),
//   {
//     type: 'line',
//     data: {
//       labels: labels,
//       datasets: [
//         {data: data}
//       ]
//     }
//   }
// );
// const bob= alert("YO YOU");

// fetch the data to populate this chart from the chart-data route
// 1. get the info from the form
// 2. use the form info to get the user's max weights
// 3. fetch to js and populate data dictionary with this info
// var dashboardChart = new Chart("workout-chart", {
//     type: "line",
//     data: {},
//     options: {}
//   });

  // first fetch- user selects exercise. post to server.
  // second fetch- GET the dictionary from the chart route and populate the JS chart
// select the exercise- triggers a fetch to server. last then
// final then= create chart 
// DONE1plop the chart into the page- dashboard- let it be there
//DONE 2 use sample data that is shaped like what we want from our route
//  DONEcopy paste what is currently there for exercise id 4 and user 2 to reflect
// 3 make a fetch request when they select an exercise from the drop down
// check that you're hitting the route that you expect to
// 4 get the info from the fetch request= exercise id, print in terminal, see that it is there
// 5 use that data and user from session to call function for max weights
// 6. move the whole code for making a chart into the final THEN in fetch, use the data that was response in fetch in place of hardcoded data
// render the chart
  

  //     fetch('/chart_data', {
  //       method: 'GET',
  //       body: JSON.stringify(formInputs),
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //     }).then((response) => {
  //         console.log(response)
  //       if (response.ok) {
  //         console.log("added")  
  //       } else {
  //         console.log(response)
  //         alert("Whoops. Fix the code, Leilani!");
  //       }
  //     });
  //   });
  // }
  






  // var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'))
  // var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
  //   return new bootstrap.Dropdown(dropdownToggleEl)
  // })

  // on change, do the fetch

// add event listener
// grab the exercise id from the element via fetch
//
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