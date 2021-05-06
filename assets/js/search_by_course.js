// SEARCH ENTERED BY RADHA AND RACHEL
// search_auto is the search box; as the user starts typing, searchCourses_auto will run
const search_auto = document.getElementById('search');
// matchlist_auto is the list of matches that gets populated by search_auto; users can click on one of the matches to add it to list
const matchList_auto = document.getElementById('match-list');

// Search courses.json and filter it
const searchCourses_auto = async searchText => {
  const res = await fetch('assets/data/courses.json');
  const course = await res.json();

  // Get matches to current text input
  let matches = Object.values(course).filter(data => {
    const regex = new RegExp(`.*(${searchText}).*`, 'gi');
    // Searches the Course Name, Nubmer, and Description; returns if there is a match
    return data.Course_Full.match(regex) || data.Course_Description.match(regex);
  });

  // If the search box is empty, the match-list will be empty as well
  if(searchText.length === 0) {
    matches = [];
    matchList_auto.innerHTML = '';
  };

  // outputHtml_auto will display matches to user
  outputHtml_auto(matches);
};

// Show results in HTML
const outputHtml_auto = matches => {
  if(matches.length > 0) {
    const html = matches.map(
      // matches to list of courses (courses.json)
      // matches become a button with onclick add function
      // onclick passes in value of button (which is the name of the course), and the ID of the button (which is the GraphDB URI)
      match =>   `
        <button class="card card-body mb-1" type="button" onclick="add_course(this.value, this.id)" value="${match.Course_Full}" id="${match.GraphDB1}"><p>${match.Course_Full}</p></button>
        `

      )
      .join('');

    // Sets match-list HTML to buttons of matches
    matchList_auto.innerHTML = html;
  }
};

// Listens for input from user (typing in search box)
search_auto.addEventListener('input', () => searchCourses_auto(search_auto.value));

// ADD AND REMOVE FUNCTION
// btnRemove is the button to remove selected courses
const btnRemove = document.querySelector('#btnRemove');
// sb is the list of selected courses
const sb = document.querySelector('#list');
// search is search box the user types into
const search = document.querySelector('#search');

// onclick function for match-list buttons
// Adds clicked on course to selected list
function add_course(name, mdb_uri){
  // validate the option
  if (name == '') {
    alert('Please enter the course name.');
    return;
  }

  // create a new option
  // name is Course Name and mdb_uri is the GraphDB URI for that course
  const option = new Option(name, mdb_uri);
  //const option = new Option(name.options[name.selectedIndex].text, name.options[name.selectedIndex].text);

  // add it to the list
  sb.add(option, undefined);

  // reset the value of the input, and returns users to keep typing in search box
  search.value = '';
  search.focus();
};

// remove selected option
btnRemove.onclick = (e) => {
  e.preventDefault();

  // save the selected option
  let selected = [];

  for (let i = 0; i < sb.options.length; i++) {
    selected[i] = sb.options[i].selected;
  }

  // remove all selected option
  let index = sb.options.length;
  while (index--) {
    if (selected[index]) {
      sb.remove(index);
    }
  }
};


// SEARCH/SUBMIT FUNCTION
// submit is the submit/search button; what users will click to show results
const submit = document.querySelector('#submit');

submit.onclick = (e) => {
  e.preventDefault();

  // create blank array to append/push to
  var submitted = [];

  // for each option is the user's list of selected courses
  $('#list option').each(function(){
      // search_uri will be set to the value of the option (which is the GraphDB URI)
      var search_uri = $(this).val();
      // Append/push URI to the array of courses
      submitted.push(search_uri);
  });

  // ensure that the list of courses the user selected has no duplicates
      var unique = [...new Set(submitted)]
      submitted = Array.from(unique)

      // searchURI function will search select classes on the GraphDB json file (our ontology)
      searchURI(submitted)
  };


  // Search GraphDB.json and filter it
  const searchURI = async searchText => {
    // Open GraphDB.json file
    const res = await fetch('assets/data/GraphDB.json');
    const json_GraphDB = await res.json();

    // results will be an array of JSON objects based on the user's search
    var results = [];
    var index;
    var current_URI;
    // html is currently used to show the results to the courseRoles.html
    var html = `<label for="results"><h1 style="font-size: 40px">Results</h1></label><br>`;

    // for each object in the searchText (each course selected)
    for (index = 0; index < searchText.length; index++) {
      // set current_URI to the current course
      current_URI = searchText[index];
      // append to the resutls array any JSON objects that match the given course URI
      results.push.apply(results, json_GraphDB.filter( record => record.Course.value === current_URI));
    };

    var unique_results = [];
    // for each JSON object in the results array
    for (index = 0; index < results.length; index++) {
      // if the role isn't already in being displayed, then display it
      if (!unique_results.includes(results[index].NICE_Role_Title.value)) {
        unique_results.push(results[index].NICE_Role_Title.value);
        html += `<button type="button" class="collapsible_button card card-body mb-1" onclick="collapsible_button_click(this.id)" id="${results[index].NICE_Role_Title.value}">${results[index].NICE_Role_Title.value}</button>
        <div class="collapse">
        <p>${results[index].NICE_Role_Description.value}</p>
        </div>
        <br>`
      };
    };

    // send html to the front end (id = test_results)
    document.getElementById('test_results').innerHTML = html;
    document.getElementById('submit').scrollIntoView({behavior: 'smooth' });
  };

// collapsible_button_click is the function that is called onclick for the collapsible buttons
function collapsible_button_click(btn_ID) {
      document.getElementById(btn_ID).classList.toggle("active");
      var collapse = document.getElementById(btn_ID).nextElementSibling;
      if (collapse.style.display === "block") {
        collapse.style.display = "none";
      } else {
        collapse.style.display = "block";
      }

};
