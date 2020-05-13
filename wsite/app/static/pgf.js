function dropdowns() {
  var body = document.getElementsByTagName("body")[0];
  var form = document.createElement("FORM");
  form.setAttribute("id", "theform")
  modes = ["Single", "Total"];
  text = ["Search for <strong>single games</strong> matching criteria",
          "Search for <strong>total games</strong> matching criteria"];
  for(val in modes){
      var d = document.createElement("DIV");
      var dropdown = document.createElement("INPUT");
      d.appendChild(dropdown);
      d.style.padding = "10px";
      d.style.backgroundColor = "lightgrey";
      d.style.width = "auto";
      d.style.margin = "0px 5px 30px 30px";
      d.style.display = "inline-block";
      form.appendChild(d);
      dropdown.setAttribute("name", "mode");
      dropdown.setAttribute("type", "radio");
      dropdown.setAttribute("value", modes[val]);
      dropdown.setAttribute("id", modes[val]);
      dropdown.style.display = "inline";
      if(modes[val] == "Single"){
        dropdown.setAttribute("checked", "checked");
        }
      var descript = document.createElement("LABEL");
      d.appendChild(descript);
      descript.setAttribute("for", modes[val]);
      descript.innerHTML = text[val];
      descript.style.display = "inline";
      descript.style.marginLeft = "5px";

  }






  var superflex = document.createElement("DIV");
  superflex.style.marginBottom = "30px";
  var flex = document.createElement("DIV");
  var flex2 = document.createElement("DIV");
  var flex3 = document.createElement("DIV");
  var flex4 = document.createElement("DIV");
  form.appendChild(superflex);
  flex.setAttribute("class", "flex-container");
  flex2.setAttribute("class", "flex-container");
  flex3.setAttribute("class", "flex-container");
  flex4.setAttribute("class", "flex-container");
  superflex.setAttribute("class", "flex-container superflex");
  superflex.appendChild(flex);
  superflex.appendChild(flex2);
  superflex.appendChild(flex3);
  superflex.appendChild(flex4);
  var seas_age = {'Seasons': [1946, 2019], 'Age': [18, 50]}
  for(var key in seas_age){
      var fieldset = document.createElement("FIELDSET");
      flex.appendChild(fieldset)
      var fieldset_legend = document.createElement("LEGEND");
      fieldset_legend.innerHTML = key;
      fieldset.appendChild(fieldset_legend);
      for(ind = 0; ind < 2; ind++){
          var dropdown = document.createElement("SELECT");
          dropdown.setAttribute("name", key + ind.toString());
          fieldset.appendChild(dropdown);
          dropdown.style.width = "40%";
          a_item = document.createElement("OPTION");
          a_item.innerHTML = "Any";
          a_item.setAttribute("value", "Any");
          dropdown.appendChild(a_item);
          for(i = seas_age[key][0]; i < seas_age[key][1]; i++){
              a_item = document.createElement("OPTION");
              dropdown.appendChild(a_item);
              if (key == "Seasons"){
                a_item.innerHTML = i.toString() + '-' + (i+1).toString().slice(-2);
                a_item.setAttribute("value", i.toString() + '-' + (i+1).toString().slice(-2));
              }
              else{
                a_item.innerHTML = i.toString();
                a_item.setAttribute("value", i.toString());
              }
          }
          if(ind == 0){
            var a = document.createElement("A");
            a.innerHTML = "to";
            a.setAttribute("class", "to_season");
            a.style.pointerEvents = "none";
            fieldset.appendChild(a);
            }
      }
  }
   var teams = {'ATL': 'ATL', 'BKN': 'BKN', 'BOS': 'BOS', 'CHA': 'CHA', 'CHI': 'CHI', 'CLE': 'CLE', 'DAL': 'DAL',
                'DEN': 'DEN', 'DET': 'DET', 'GSW': 'GSW', 'HOU': 'HOU', 'IND': 'IND', 'LAC': 'LAC', 'LAL': 'LAL', 'MEM': 'MEM',
                'MIA': 'MIA', 'MIL': 'MIL', 'MIN': 'MIN', 'NOP': 'NOP', 'NYK': 'NYK', 'OKC': 'OKC', 'ORL': 'ORL', 'PHI': 'PHI',
                'PHX': 'PHX', 'POR': 'POR', 'SAC': 'SAC', 'SAS': 'SAS', 'TOR': 'TOR', 'UTA': 'UTA', 'WAS': 'WAS'};

   var single_dropdowns = {"Game_Month": {"October": 10, "November": 11, "December": 12, "January": 1,
                                     "February": 2, "March": 3, "April": 4, "May": 5, "June": 6},
                           "Team": sorting(teams), "Opponent": sorting(teams)};
  for(var key in single_dropdowns){
      var fieldset = document.createElement("FIELDSET");
      flex2.appendChild(fieldset)
      var fieldset_legend = document.createElement("LEGEND");
      fieldset_legend.innerHTML = key.split("_").join(" ");
      fieldset.appendChild(fieldset_legend);
      var dropdown = document.createElement("SELECT");
      dropdown.setAttribute("name", key);
      fieldset.appendChild(dropdown);
      dropdown.style.width = "40%";
      a_item = document.createElement("OPTION");
      a_item.innerHTML = (key == "Game_Month") ? "All Months": "All Teams";
      a_item.setAttribute("value", "Any");
      dropdown.appendChild(a_item);
      for(subkey in single_dropdowns[key]){
          a_item = document.createElement("OPTION");
          dropdown.appendChild(a_item);
          a_item.innerHTML = subkey;
          a_item.setAttribute("value", single_dropdowns[key][subkey]);
          }
      }
  var radios = {"Game_Type": ["Regular Season", "Playoffs", "Either"],
                "Game_Result": ["Won", "Lost", "Either"],
                "Role": ["Starter", "Reserve", "Either"],
                "Game_Location": ["Home", "Away", "Either"],
                };
  for(var key in radios){
     var fieldset = document.createElement("FIELDSET");
     if(key == "Game_Type"){
        flex.appendChild(fieldset);
     }
     else{
     flex3.appendChild(fieldset);
     }
     var fieldset_legend = document.createElement("LEGEND");
     fieldset_legend.innerHTML = key.split("_").join(" ");
     fieldset.appendChild(fieldset_legend);
     for(var field in radios[key]){
          var fielddiv = document.createElement("DIV");
          fielddiv.setAttribute("class", "fielddiv");
          var dropdown = document.createElement("INPUT");
          fielddiv.appendChild(dropdown);
          dropdown.setAttribute("name", key);
          dropdown.setAttribute("type", "radio");
          dropdown.setAttribute("value", radios[key][field]);
          dropdown.setAttribute("id", key+radios[key][field]);
          if (radios[key][field] == "Either"){ dropdown.setAttribute("checked", "checked");}
          dropdown.style.marginLeft = "5px";
          fieldset.appendChild(fielddiv);
          var descript = document.createElement("LABEL");
          fielddiv.appendChild(descript);
          descript.setAttribute("for", key+radios[key][field]);
          descript.innerHTML = radios[key][field];
          descript.style.marginLeft = "5px";
          fieldset.appendChild(descript);
          fieldset.appendChild(document.createElement("BR"));
     }
  }
  droppies = {"stats": ['MIN', 'FGM', 'FGA', 'FG PCT', 'FG3M', 'FG3A', 'FG3 PCT', 'FTM', 'FTA', 'FT PCT', 'OREB',
               'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS'],
               "operators": ["<="]};
  var fieldset = document.createElement("FIELDSET");
  flex4.appendChild(fieldset);
  var fieldset_legend = document.createElement("LEGEND");
  fieldset_legend.innerHTML = "Additional Criteria";
  fieldset.appendChild(fieldset_legend);
  for(i = 0; i < 4; i++){
      var additional_div = document.createElement("DIV");
      additional_div.setAttribute("class", "additional_div")
      fieldset.appendChild(additional_div)
      for(var key in droppies){
        var dropdown = document.createElement("SELECT");
        dropdown.setAttribute("name", key+i.toString());
        additional_div.appendChild(dropdown);
        dropdown.style.width = (key == "stats") ? "30%": "20%";
        a_item = document.createElement("OPTION");
        a_item.innerHTML = (key == "stats") ? "Choose":">="
        a_item.setAttribute("value", (key == "stats") ? "Any":"gt");
        dropdown.appendChild(a_item);
        for(var subkey in droppies[key]){
            a_item = document.createElement("OPTION");
            dropdown.appendChild(a_item);
            a_item.innerHTML = droppies[key][subkey];
            a_item.setAttribute("value", (key == "stats") ? droppies[key][subkey]: "lt");
            }
      }
      var input = document.createElement("INPUT");
      additional_div.appendChild(input);
      input.setAttribute("class", "additional_input");
      input.setAttribute("name", "input"+i.toString());
      input.setAttribute("type", "text");
      input.style.width
      additional_div.appendChild(document.createElement("BR"));
  }

  a_item = document.createElement("A");
  a_item.innerHTML = "<strong>" + "Sort By:" + "</strong>";
  a_item.style.pointerEvents = "none";
  a_item.style.width = "25%";
  a_item.style.margin = "10px";
  a_item.style.marginBottom = "0px";
  a_item.style.padding = "10px";
  a_item.style.color = "black";
  b_item = document.createElement("A");
  b_item.setAttribute("class", "dynamic Total");
  b_item.innerHTML = "<strong>" + " Total Occurrences" + "</strong>";
  b_item.style.pointerEvents = "none";
  b_item.style.width = "25%";
  b_item.style.margin = "10px";
  b_item.style.marginBottom = "0px";
  b_item.style.padding = "10px";
  b_item.style.color = "black";
  fieldset.appendChild(a_item);
  fieldset.appendChild(b_item);
  b_item.style.display = "none";
  var dropdown = document.createElement("SELECT");
  dropdown.setAttribute("name", "order");
  dropdown.setAttribute("class", " dynamic Single");
  fieldset.appendChild(dropdown);
  for(var subkey in droppies["stats"]){
    a_item = document.createElement("OPTION");
    dropdown.appendChild(a_item);
    a_item.innerHTML = droppies["stats"][subkey];
    a_item.setAttribute("value", droppies["stats"][subkey]);
    }

  fieldset.appendChild(document.createElement("BR"));
  submit = document.createElement("INPUT");
  submit.setAttribute("type", "submit");
  submit.setAttribute("value", "Get Results");
  submit.style.backgroundColor = "#4CAF50";
  submit.style.color = "white";
  submit.style.padding = "10px";
  submit.style.margin = "10px";
  fieldset.appendChild(submit);
  body.appendChild(form);
  document.getElementById('theform').onsubmit = function(){
    window.location = '/pgf/find?' + $(document.getElementById('theform')).serialize() + "&page=1";
    return false;
  };

   $(function(){
       $("input[name=mode]").click(function(){
          $(".dynamic").not("."+this.value).hide();
          $("."+this.value).show();
       });
   });

}

function sorting(obj){
    var keys = [];
    var sorted_obj = {};

    for(var key in obj){
        if(obj.hasOwnProperty(key)){
            keys.push(key);
        }
    }

    // sort keys
    keys.sort();

    // create new array based on Sorted Keys
    jQuery.each(keys, function(i, key){
        sorted_obj[key] = obj[key];
    });

    return sorted_obj;
};
