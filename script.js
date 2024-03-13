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



document.addEventListener('DOMContentLoaded', function () {
  const menuIcon = document.querySelector('.menu-icon');
  const navItems = document.querySelector('.nav-list');
  const listItems = document.querySelectorAll('.nav-list li');

  menuIcon.addEventListener('click', function () {
      navItems.classList.toggle('show');
  });

  

  listItems.forEach(function (item) {
      item.addEventListener('click', function () {
          menuIcon.click(); // Simulate a click on the menu icon to close the menu
      });
  });
});