'use strict'

// TODO: Create a function that takes in the API and creates the elements needed
// cross site scripting: BEWAREEEEEE
// make API request in server
// results via fetch-get to display info
// fetch-post to take info to server to create records

// Prevents redirect upon clicking the Schedule Workout Link of Navigation Bar. Calendar form will drop down instead.
const scheduleWorkout = document.querySelector('#schedule-workout-link');
scheduleWorkout.addEventListener('click', (evt) => {
  evt.preventDefault();
  const showCalendar = document.getElementById('schedule-workout');
  console.log(showCalendar.display)
  if (scheduleWorkout.innerHTML == "Schedule Workout") {
    showCalendar.style.display = 'block';
    scheduleWorkout.innerHTML = "Hide Calendar";
  } 
  else if (scheduleWorkout.innerHTML == "Hide Calendar") {
    showCalendar.style.display = "none";
    scheduleWorkout.innerHTML = "Schedule Workout";
  }
});

const addButtons = document.querySelectorAll('.add-to-workout');
for (const button of addButtons) {
  button.addEventListener('click', (evt) => {
    evt.preventDefault();  
    const numSets = prompt('How many sets would you like to do?');
    
    const formInputs = {
      numberOfSets: parseInt(numSets),
      exercise_id: button.id,
      exercise_name: document.getElementById(`exercise-name-${button.id}`).value,
      exercise_description : document.getElementById(`exercise-description-${button.id}`).value
    };

    fetch('/add_to_workout', {
      method: 'POST',
      body: JSON.stringify(formInputs),
      headers: {
        'Content-Type': 'application/json',
      },
    }).then((response) => {
        console.log(response)
      if (response.ok) {
        console.log("added")  
      } else {
        console.log(response)
        alert("Whoops. Fix the code, Leilani!");
      }
    });
  });
}
