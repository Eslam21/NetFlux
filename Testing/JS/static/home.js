const APIURL =
  "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=04c35731a5ee918f014970082a0088b1&page=1";

const IMGPATH = "https://image.tmdb.org/t/p/w1280";

const SEARCHAPI =
  "https://api.themoviedb.org/3/search/movie?&api_key=04c35731a5ee918f014970082a0088b1&query=";

const main = document.getElementById("main");
const form = document.getElementById("form");
const search = document.getElementById("search");
const mobileMenu = document.querySelector(".mobile-menu");
const menuButton = document.querySelector(".openmenu");
const closeButton = document.querySelector(".closemenu");
const starParent = document.querySelector(".starRating");

menuButton.addEventListener("click", () => {
  mobileMenu.classList.add("active");
  document.body.style.overflow = "hidden";
});

closeButton.addEventListener("click", () => {
  mobileMenu.classList.remove("active");
  document.body.style.overflow = "visible";
});


  showMovies();


class Stars {
  constructor(className, numOfRating) {
    (this.className = className), (this.isValid = false);
    this.numOfRating = numOfRating;
    this.rating = [{ id: 1 }, { id: 2 }, { id: 3 }, { id: 4 }, { id: 5 }];
    this.starContainer = null;
    this.starContainer = document.querySelector(className);
    this.toggleId = 0;

    try {
      if (this.starContainer) {
        this.isValid = true;
        this.className = this.className;
      } else {
        this.isValid = false;
        throw new Error(`className ${this.className} is not valid`);
      }
    } catch (e) {
      console.log(e.message);
    }
    if (this.isValid && numOfRating >= 0) {
      this.init();
    }
  }

  init() {
    const ul = document.createElement("ul");
    const fragment = document.createDocumentFragment();

    ul.classList.add("ul-stars");
    ul.style.listStyleType = "none";
    // ul.style.display = "flex";
    // ul.style.margin = "0px";
    // ul.style.padding = "0px";

    const stars = this.rating.map((star) => {
      const li = document.createElement("li");
      const a = document.createElement("a");

      li.style.margin = "3px";
      a.style.fontSize = "54px";
      a.style.cursor = "pointer";
      a.innerHTML = "&#9734";
      a.style.color = "#ffffffad";
      a.id = star.id;

      if (a.id <= this.numOfRating) {
        a.innerHTML = "&#9733";
      }

      a.addEventListener("click", (e) => {
        this.setRating(ul, e);
      });

      li.appendChild(a);
      fragment.appendChild(li);
      return li;
    });

    ul.appendChild(fragment);
    console.log(ul, "uls====");
    this.starContainer.appendChild(ul);
  }

  setRating(ul, e) {
    const liList = ul.querySelectorAll("li");

    const currentEl = Number(e.target.id);
    if (this.toggleId !== currentEl) {
      for (const li of liList) {
        const a = li.querySelector("a");
        this.toggleId = currentEl;

        if (a.id <= currentEl) {
          a.innerHTML = "&#9733";
        } else {
          a.innerHTML = "&#9734";
        }
      }
    } else {
      for (const li of liList) {
        const a = li.querySelector("a");

        a.innerHTML = "&#9734";
        this.toggleId = 0;
      }
    }
  }
}

function showMovies() {
  var movies = JSON.parse('{{ movies | tojson | safe}}');
  var title = JSON.parse('{{ title | tojson | safe}}');
  var poster_path = JSON.parse('{{ path | tojson | safe}}');
  var vote_average = JSON.parse('{{ rating | tojson | safe}}');
  var overview = JSON.parse('{{ Overview | tojson | safe}}');
  var id = JSON.parse('{{ id | tojson | safe}}');
  
  main.innerHTML = "";
  for(let i=0; i<=movies.length; i++) {
    
    let className = "stars-container" + index;
    const movieEl = document.createElement("div");
    movieEl.classList.add("movie");

    movieEl.innerHTML = `
      <img src="${IMGPATH + poster_path[i]}" alt="${title[i]}"/>

     <div class="movie-info">
        <h3>${title}</h3>
        <span class="${getClassByRate(vote_average[i])}">${vote_average[i]}</span>
     </div> 

     <div class="overview">
     <h2>Overview:</h2>
     ${overview[i]}
     </div>
     <nav class="menu">
        
          <button class="myButton" id="watch${id[i]}"><ion-icon name="eye"></ion-icon></button>
          <button class="myButton" id="heart${id[i]}"><ion-icon name="heart"></ion-icon>
          <button class="myButton" id="later${id[i]}"><ion-icon name="time"></ion-icon></ion-icon></button>
     </nav>
     <div class="rating-container">
      <div id='stars-container' class=${className}></div>
     </div>
     `;
    main.appendChild(movieEl);
    const star2 = new Stars("." + className, 0);
    let watchId = document.getElementById(`watch${id[i]}`);
    let heartId = document.getElementById(`heart${id[i]}`);
    let laterId = document.getElementById(`later${id[i]}`);
    watchId.addEventListener("click", () => {
      if (watchId.style.color === "") {
        watchId.style.color = "cyan";
      } else {
        watchId.style.color = "";
      }
    });

    heartId.addEventListener("click", () => {
      if (heartId.style.color === "") {
        heartId.style.color = "red";
      } else {
        heartId.style.color = "";
      }
    });

    laterId.addEventListener("click", () => {
      if (laterId.style.color === "") {
        laterId.style.color = "white";
      } else {
        laterId.style.color = "";
      }
    });
  });
}

function showRating() {
  let selectedRating = 0;
  for (const star of starParent.children) {
    const id = star.id.replace("star", "");

    star.addEventListener("mouseover", () => {
      for (let i = 0; i < id; i++) {
        starParent.children[i].style.fill = "#ffe88c";
      }
    });

    star.addEventListener("mouseout", () => {
      for (const str of starParent.children) {
        if (!str.isClicked) {
          str.style.fill = "#353535";
        }
      }
    });

    star.addEventListener("click", () => {
      if (selectedRating === id) {
        for (const str of starParent.children) {
          str.style.fill = "#353535";
          str.isClicked = false;
        }

        selectedRating = 0;
      } else {
        for (let i = 0; i < id; i++) {
          starParent.children[i].isClicked = true;
        }

        for (let i = id; i < starParent.children.length; i++) {
          starParent.children[i].style.fill = "#353535";
          starParent.children[i].isClicked = false;
        }

        selectedRating = id;
        console.log(`your rating: ${id}/${starAmount}`);
      }
    });
  }
}

function getClassByRate(vote) {
 
 return "white"
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const searchTerm = search.value;

  if (searchTerm) {
    getMovies(SEARCHAPI + searchTerm);

    search.value = "";
  }
});

// For the thumbnail demo! :]

var count = 1;
setTimeout(demo, 500);
setTimeout(demo, 700);
setTimeout(demo, 900);
setTimeout(reset, 2000);

setTimeout(demo, 2500);
setTimeout(demo, 2750);
setTimeout(demo, 3050);

var mousein = false;
function demo() {
  if (mousein) return;
  document.getElementById("demo" + count++).classList.toggle("hover");
}

function demo2() {
  if (mousein) return;
  document.getElementById("demo2").classList.toggle("hover");
}

function reset() {
  count = 1;
  var hovers = document.querySelectorAll(".hover");
  for (var i = 0; i < hovers.length; i++) {
    hovers[i].classList.remove("hover");
  }
}

document.addEventListener("mouseover", function () {
  mousein = true;
  reset();
});
