'use strict'


// Show exercises associated with the selected main muscle
// When the muscle group is clicked, search the exercise API for exercises under that muscle group



// Send a GET request to the API to READ a list of exercises

// send a GET request to the exercise/:id to READ(view) an exercise
// send  GET request to /workout_log to READ a list of workouts


// Send a POST request to /workout_log to CREATE a new workout
    //event listener for click of schedule_workout link
    //stop default (page refresh)
    //update page with HTML calendar to schedule workout
    //on submission, route to /schedule_workout to check for existing scheduled workout, or add to db
    //all render in user dashboaord

// create today's date formatted, so that it can set the default date in the date form to schedule workout
const today = new Date();
function formatDate(date, format) {
    const formatting = {
        mm: date.getMonth() + 1,
        dd: date.getDate(),
        yyyy: date.getFullYear(),
        yy: date.getFullYear().toString().slice(-2)
        
    }
    return format.replace(/mm|dd|yyyy|yy/gi, matched => formatting[matched])
}

const dateToday = formatDate(today, "yyyy-mm-dd");
dateToday.padded(10,"0")
// !DEBUG: for some reason this isn't populating the form 
document.querySelector("#cal-to-schedule-workout").setAttribute("value", `"${dateToday}"`);
// create form that renders when schedule workout link is clicked in user dashboard
const showCalendar = document.querySelector("#schedule-workout-link");

showCalendar.addEventListener('click', (evt) => {
    evt.preventDefault();
    document.querySelector("#body").insertAdjacentHTML('beforeend',
    `<form action="/schedule_workout">
        <label for="schedule-workout">
            Schedule Workout
        </label>
        <input type="date" id="cal-to-schedule-workout" name="schedule-workout" value="${dateToday}">
        <p><button>Submit</button></p>
    </form>
    `);
});
    

// Send a PUT request to /workout_log to UPDATE a workout via workout_logs

// send a DELETE request to /workout_log/:id to DELETE a workout or exercise from the workout

// For Fun- CSS styling for a sliding log in screen
// const signUpButton = document.getElementById('signUp');
// const signInButton = document.getElementById('signIn');
// const logContainer = document.getElementById('log-container');

// signUpButton.addEventListener('click', ()=> 
//     logContainer.classList.add('right-panel-active')
// );

// signInButton.addEventListener('click', ()=> 
//     logContainer.classList.remove('right-panel-active')
// );

// Show exercises related to muscle selected
const selectedMuscle = document.getElementById('')

//ajax request to view description of muscle exercises
// get the muscle id when clicked, then add HTML that includes t
// function viewExerciseDetails()
// const exerciseName = 
// const onClick = (event) => {



// // const onClick = (event) => {
// //     if (event.target.nodeName)
// // }
// // function showExercisesByMuscleId(evt) {
// //     evt.target.getAttribute('')
// //     const muscle_id = document.querySelector('.')
// // }
// // document.querySelector("muscle_id").addEventListener('click', () => {
// //     fetch('exercise_details/?muscle_id=<muscle_id>')
// //         .then((response) => response.json())
// //         .then((result) => {
// //             const exercise_name = result['name'];
// //             const exercise_description = result['description'];
// //             document.querySelector('').insertAdjacentHTML('beforeend', 
// //             <div> 

// //             </div>)
// //         })
// // })
// //     fetch('/muscle/?muscle_id=<muscle_id>')
// const express = require('express')
// const app = express();

// app.get('/exercises', (req,res)=> {
//     res.json({greeting: "here idk what i'm doing"})
// });


