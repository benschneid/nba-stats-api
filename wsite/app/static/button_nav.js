function buttons(prev, next, page){
    var body = document.getElementsByTagName("body")[0];
    string_url = window.location.toString();
    if(prev){
        var a = document.createElement("A");
        a.innerHTML = "Previous page";
        new_url = string_url.substring(0, string_url.indexOf("page=")) + "page=" + (page-1).toString();
        a.setAttribute("href", new_url);
        a.style.float = "left";
        a.style.marginLeft = "30px";
        a.style.marginBottom = "30px";
        a.style.color = "blue";
        body.appendChild(a);
    }
    if(next){
        var a = document.createElement("A");
        a.innerHTML = "Next page";
        new_url = string_url.substring(0, string_url.indexOf("page=")) + "page=" + (page+1).toString();
        a.setAttribute("href", new_url);
        a.style.marginLeft = "30px";
        a.style.marginBottom = "30px";
        if(!prev){
             a.style.float = "left";
        }
        a.style.color = "blue";
        body.appendChild(a);
    }

}