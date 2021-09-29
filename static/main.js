const toggleCollapse = document.querySelector('.toggle-collapse span');
const nav = document.querySelector('.nav');

// Onclick event on toggle Collapse span tag
toggleCollapse.onclick = () => {
    nav.classList.toggle('collapse');
};

// Only allow 1-3 options for food flavor choices
$(document).ready(function()
{
    var flavorcheck = $("input.flavor[type='checkbox']");

    flavorcheck.click(function(e) {
    if (flavorcheck.filter(":checked").length > 3)
    {
    e.preventDefault();
    }
    else if (flavorcheck.filter(":checked").length < 1)
    {
      e.preventDefault();
    }
});
});