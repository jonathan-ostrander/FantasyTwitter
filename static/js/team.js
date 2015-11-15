$("button.login").click(function(e) {
  e.preventDefault();
  var checked = [];
  $("input:checkbox:checked").each(function(){
    checked.push($(this).val());
  });
  window.location.href = "/createteam?check=" + checked.join("|");
});

$("button#delete").click(function(e) {
  e.preventDefault();
  window.location.href = "/deleteteam";
});
