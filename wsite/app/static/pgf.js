function dropdowns() {
  // get the reference for the body
  var body = document.getElementsByTagName("body")[0];
  var form = document.createElement("FORM");
  form.setAttribute("id", "theform")
  var flex = document.createElement("DIV");
  form.appendChild(flex);
  flex.setAttribute("class", "flex-container");
  var seas_age = {'Seasons': [1946, 2020], 'Age': [18, 50]}
  for(var key in seas_age){
      var fieldset = document.createElement("FIELDSET");
      flex.appendChild(fieldset)
      var fieldset_legend = document.createElement("LEGEND");
      fieldset_legend.innerHTML = key;
      fieldset.appendChild(fieldset_legend);
      for(ind = 0; ind < 2; ind++){
          var dropdown = document.createElement("DIV");
          fieldset.appendChild(dropdown)
          dropdown.setAttribute("class", "dropdown dropdown-button");
          dropdown.setAttribute("name", key+ind.toString());
          var dropdown_toggle = document.createElement("BUTTON");
          dropdown_toggle.style.width = "100px";
          dropdown_toggle.innerHTML = "Any ";
          dropdown.appendChild(dropdown_toggle);
          dropdown_toggle.setAttribute("class", "btn btn-primary dropdown-toggle");
          dropdown_toggle.setAttribute("data-toggle", "dropdown");
          var dropdown_span = document.createElement("SPAN");
          dropdown_toggle.appendChild(dropdown_span);
          dropdown_span.setAttribute("class", "caret");
          var dropdown_menu = document.createElement("UL");
          dropdown_menu.setAttribute("class", "dropdown-menu parameter");
          dropdown.appendChild(dropdown_menu);
          var list_item = document.createElement("LI");
          dropdown_menu.appendChild(list_item);
          var a_item = document.createElement("A");
          a_item.style.textAlign = "center";
          list_item.appendChild(a_item);
          a_item.innerHTML = "Any";
          a_item.value = "Any";
          for(i = seas_age[key][0]; i < seas_age[key][1]; i++){
              var list_item = document.createElement("LI");
              dropdown_menu.appendChild(list_item);
              var a_item = document.createElement("A");
              a_item.style.textAlign = "center";
              list_item.appendChild(a_item);
              if (key == "Seasons"){
                a_item.innerHTML = i.toString() + '-' + (i+1).toString().slice(-2);
              }
              else{
                a_item.innerHTML = i.toString()
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
   submit = document.createElement("INPUT");
   submit.setAttribute("type", "submit");
   submit.setAttribute("value", "Get Results");
   form.appendChild(submit);
   body.appendChild(form);
   $(".dropdown-menu li a").click(function(){
   $(this).parents(".dropdown").find('.btn').html($(this).text() + ' <span class="caret"></span>');
   $(this).parents(".dropdown").find('.btn').val($(this).data('value'));
   });
   document.getElementById('theform').onsubmit = function() {
    window.location = '/' + $('theform').serialize();
    return false;
    };

}

function dropdowns2() {
  // get the reference for the body
  var body = document.getElementsByTagName("body")[0];
  var form = document.createElement("FORM");
  form.setAttribute("id", "theform")
  var flex = document.createElement("DIV");
  form.appendChild(flex);
  flex.setAttribute("class", "flex-container");
  var seas_age = {'Seasons': [1946, 2020], 'Age': [18, 50]}
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
          dropdown.style.width = "100px";
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
   submit = document.createElement("INPUT");
   submit.setAttribute("type", "submit");
   submit.setAttribute("value", "Get Results");
   form.appendChild(submit);
   body.appendChild(form);
   document.getElementById('theform').onsubmit = function() {
    window.location = '/pgf/find?' + $(document.getElementById('theform')).serialize();
    return false;
    };

}
