var modal = document.getElementById("myModal");
    
var btn = document.getElementById("showForm");

var span = document.getElementById("closeForm");

btn.onclick = function () {
  modal.style.display = "block";
};

span.onclick = function () {
  modal.style.display = "none";
};

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
};


// Pop up...