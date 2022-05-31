'use strict'

// Allows users to delete extraneous or unnecessary logs. 
const deleteButtons = document.querySelectorAll('.delete-log');
for (const button of deleteButtons) {
  button.addEventListener('click', (evt) => {
    
    const logId = button.id
    // evt.preventDefault();
    console.log(evt);
    const log_to_delete = {
      log_id: logId
    }
    console.log(log_to_delete);
    fetch('/delete_log', {
      method: 'DELETE',
      body: JSON.stringify(log_to_delete),
      headers: {
        'Content-Type': 'application/json'
      },
    }).then((response) => {
      console.log(response);
      console.log(`here is the log to delete: ${log_to_delete}`);
      if (response.ok) {
        console.log("deleted");
        document.getElementById(`div-${logId}`).remove;
      } else {
        console.log(response);
      }
    })
  })
};

const editButtons = document.querySelectorAll('.update-log')
for (const button of editButtons) {
  button.addEventListener('click', (evt) => {
    // prevent page refresh or redirect upon clicking update log button
    evt.preventDefault();
    console.log(evt);
    const logId = button.id;
    const log_update_inputs={
      // why is this returning as NULL??? querySelector and getElementById are both showing up as Null
      weight: document.getElementById(`weight-${logId}`).value,
      num_of_reps: document.getElementById(`num-of-reps-${logId}`).value,
      weight_unit: document.getElementById(`weight-unit-${logId}`).selectedOptions[0].value,
      log_id: logId
    };
    console.log(log_update_inputs)
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

