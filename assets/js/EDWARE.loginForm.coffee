#global define
define [
  "jquery"
], ($) ->
  
  $(document).ready ->
    count = 0
    $("form").submit ->
      if $("#inputEmail").val() is ""
        $("#inputEmail").closest(".control-group").addClass "error"
        count++
      else 
        $("#inputEmail").closest(".control-group").removeClass "error"
        
      if $("#inputPassword").val() is ""
        $("#inputPassword").closest(".control-group").addClass "error"
        count++
      else
        $("#inputPassword").closest(".control-group").removeClass "error"
        
      return false if count > 0
      
      location.href = "/assets/html/studentList.html?districtId=4&schoolId=3&asmtGrade=1"
      false
