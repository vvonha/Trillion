$("#password").on("focusout", function () {
    if ($(this).val() != $("#password2").val()) {
      $("#password2").removeClass("valid").addClass("invalid");
    } else {
      $("#password2").removeClass("invalid").addClass("valid");
    }
  });
  
  $("#password2").on("keyup", function () {
    if ($("#password").val() != $(this).val()) {
      $(this).removeClass("valid").addClass("invalid");
    } else {
      $(this).removeClass("invalid").addClass("valid");
    }
  });