function generate_table(data, headers, order) {
  // get the reference for the body
  var body = document.getElementsByTagName("body")[0];

  // creates a <table> element and a <tbody> element
  var tbl = document.createElement("table");
  var tblBody = document.createElement("tbody");

  // creating header row
  if(data.length > 0){
    createHeader(headers,tblBody)
    }

  // creating all cells
  var counter = 0;
  for (var i = 0; i < data.length; i++) {
    // creates a table row
    if(i%25 == 0 && i > 0){
        createHeader(headers, tblBody);
    }
    var row = document.createElement("tr");
    tblBody.appendChild(row);
    if(i > 0 && data[i][0] == data[i-1][0]){
      row.style.color = "#808080"
    }
    for (var j = 0; j < headers.length; j++) {
      // Create a <td> element and a text node, make the text
      // node the contents of the <td>, and put the <td> at
      // the end of the table row
      var cell = document.createElement("td");
      cell.style.padding = "2px";
      cell.style.textAlign = "center";
      if(order){
        if(j == order){
            cell.style.backgroundColor = "orange";
        }
        if(j == 1){
            var cellText = document.createElement("A");
            cellText.innerHTML = data[i][j];
            cellText.setAttribute("href", "/players/" + data[i][data[i].length-1].toString());
            cell.appendChild(cellText);
            row.appendChild(cell);
            continue;
        }
      }
      var cellText = document.createTextNode(data[i][j]);
      cell.appendChild(cellText);
      row.appendChild(cell);
    }

    // add the row to the end of the table body
  }

  // put the <tbody> in the <table>
  tbl.appendChild(tblBody);
  // appends <table> into <body>
  body.appendChild(tbl);
  // sets the border attribute of tbl to 2;
  tbl.setAttribute("border", "2");
  tbl.style.marginLeft = "30px";
  tbl.style.marginBottom = "30px";
}

function createHeader(headers,tblBody){
  var row = document.createElement("tr");
  row.style.backgroundColor = "#D3D3D3";
//  row.style.color = "red";
  row.style.fontWeight = "bold";
  for (var j = 0; j < headers.length; j++) {
    var cell = document.createElement("td");
    var cellText = document.createTextNode(headers[j]);
    cell.appendChild(cellText);
    cell.style.padding = "2px";
    cell.style.textAlign = "center";
    row.appendChild(cell);
  }
  tblBody.appendChild(row);
}