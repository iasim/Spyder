//SEARCH ENTERED BY RADHA
const search_auto = document.getElementById('search');
const matchList_auto = document.getElementById('match-list');

// Search courses.json and filter it
const searchCourses_auto = async searchText => {
  const res = await fetch('assets/data/courses.json');
  const course = await res.json();

  //get matches to current text input
  let matches = Object.values(course).filter(data => {
    const regex = new RegExp(`.*(${searchText}).*`, 'gi');
    return data.Course_Full.match(regex) || data.Course_Description.match(regex);
  });

  if(searchText.length === 0) {
    matches = [];
    matchList_auto.innerHTML = '';
  };

  outputHtml_auto(matches);
};

//Show results in html
const outputHtml_auto = matches => {
  if(matches.length > 0) {
    const html = matches.map(
      match =>   `
        <button class="card card-body mb-1" type="button" onclick="add_course(this.value)" value="${match.Course_Full}"><p>${match.Course_Full}</p></button>
        `
      )
      .join('');

      const mongo_URI = matches.map(
        match =>   `"${match.GraphDB1}"`
        )
        .join(',');

    matchList_auto.innerHTML = html;
  }
};

search_auto.addEventListener('input', () => searchCourses_auto(search_auto.value));


//ADD AND REMOVE FUNCTION
const btnRemove = document.querySelector('#btnRemove');
const sb = document.querySelector('#list');
const search = document.querySelector('#search');

function add_course(name){
  // validate the option
  if (name == '') {
    alert('Please enter the name.');
    return;
  }
  // create a new option
  //const option = new Option(name.options[name.selectedIndex].text, name.options[name.selectedIndex].text);
  const option = new Option(name, name);
  // add it to the list
  sb.add(option, undefined);

  // reset the value of the input
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
