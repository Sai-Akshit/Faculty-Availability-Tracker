function classToggle() {
    const navs = document.querySelectorAll('.Navbar__Items')
    navs.forEach(nav => nav.classList.toggle('Navbar__ToggleShow'));
  }
  
  document.querySelector('.Navbar__Link-toggle')
    .addEventListener('click', classToggle);
        $(document).ready(function() {
       $("img").on("contextmenu",function(){
          return false;
       }); 
   });