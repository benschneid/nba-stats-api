function dropdowns(){
    document.getElementById('form').onsubmit = function(){
        if(document.getElementById("player1_header").style.display == "none" ||
            document.getElementById("player2_header").style.display == "none"){
                alert("Please select two players!");
            }
        else {
            document.getElementById("player1_header").style.display = "none";
            document.getElementById("player2_header").style.display = "none";
            document.getElementById("player1_x").style.display = "none";
            document.getElementById("player2_x").style.display = "none";
            document.getElementById("player1").style.display = "initial";
            document.getElementById("player2").style.display = "initial";
            window.location = '/h2h/find?' + $(document.getElementById('form')).serialize();
            document.getElementById("player1").value = "";
            document.getElementById("player2").value = "";
        }
        return false;
    };
}