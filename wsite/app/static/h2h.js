document.getElementById('form').onsubmit = function(){
window.location = '/h2h/find?' + $(document.getElementById('form')).serialize();
return false;
};