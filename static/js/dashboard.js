'use strict'

var dashboardChart = new Chart("workout-chart", {
    type: "line",
    data: {},
    options: {}
  });


  var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'))
  var dropdownList = dropdownElementList.map(function (dropdownToggleEl) {
    return new bootstrap.Dropdown(dropdownToggleEl)
  })