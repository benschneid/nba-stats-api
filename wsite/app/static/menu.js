function autocomplete(inp, arr, from_years, to_years, ids, parent, selected, bb) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  dic = {};
  for(i in ids){
    dic[ids[i]] = arr[i];
  }
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      if(inp.name == "myCountry"){
        a.setAttribute("class", "autocomplete-items");
      }
      else{
        a.setAttribute("class", "autocomplete-items h2h");
      }
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        var split = arr[i].split(" ");
        for(j = 0; j < split.length; j++){
            ind = arr[i].indexOf(split[j])
        /*check if the item starts with the same letters as the text field value:*/
            if (arr[i].substr(ind, val.length).toUpperCase() == val.toUpperCase()) {
              /*create a DIV element for each matching element:*/
              b = document.createElement("DIV");
              if(inp.name == "myCountry"){
                b.href = "/players/" + ids[i];
              }
              /*make the matching letters bold:*/
              b.innerHTML = arr[i].substr(0, ind);
              b.innerHTML += "<strong>" + arr[i].substr(ind, val.length) + "</strong>";
              b.innerHTML += arr[i].substr(ind + val.length);

              years = document.createElement("A");
              years.innerHTML = " " + from_years[i] + "-" + to_years[i];
              years.style.float = "right";
              years.style.pointerEvents = "none";
              b.appendChild(years);
              /*insert a input field that will hold the current array item's value:*/
              b.innerHTML += "<input type='hidden' value='" + ids[i] + "'>";
              /*execute a function when someone clicks on the item value (DIV element):*/
              b.addEventListener("click", function(e) {
                  /*insert the value for the autocomplete text field:*/
                  inp.value = this.getElementsByTagName("input")[0].value;
                  /*close the list of autocompleted values,
                  (or any other open lists of autocompleted values:*/
                  closeAllLists();
                  if(this.href){
                    inp.value = "";
                    window.location = this.href;
                  }
                  else{
                    inp.style.display = "none";
                    selected.style.display = "inline";
                    selected.innerHTML = "Selected: "+ "<strong>"+ dic[inp.value] +"</strong>";
                    bb.style.display = "inline";
                    bb.addEventListener("click", function() {
                        bb.style.display = "none";
                        selected.style.display = "none";
                        inp.style.display = "initial";
                        inp.value=null;
                    });
                  }
              });
              a.appendChild(b);
            }
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
/*autocomplete(document.getElementById("myInput"), countries);*/