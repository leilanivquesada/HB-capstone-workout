'use strict'


const viewLinks = document.querySelectorAll('.to-update')
for (const link of viewLinks) {
  link.addEventListener('click', (evt) => {
    // prevent page refresh or redirect upon clicking update log button
    evt.preventDefault();
    console.log(evt);
    
    const workout_date={
      // why is this returning as NULL??? querySelector and getElementById are both showing up as Null
      date_of_scheduled_workout: link.id
    };
    console.log(workout_date_update)
    fetch('/update_workout_log', {
      method: 'POST',
      body: JSON.stringify(log_update_inputs),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then((response) => {
      console.log(response)
      console.log(log_update_inputs)
      if (response.ok) {
        console.log("updated")
        document.querySelector(`span.status-${logId}`).innerHTML = "Log updated!"
      } else {
        console.log(response)
        document.querySelector(`span.status-${logId}`).innerHTML = "Log not updated!"
        alert("Leilani! There's an error!")
      }
    });
  });
}

