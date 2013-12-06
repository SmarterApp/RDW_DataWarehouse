require ["jquery"], ($) ->
  # load pdf
  url = document.URL.replace("print", "indivStudentReport")
  url = url.replace("/assets/html/","/services/pdf/").replace(new RegExp("#.*"),"")
  window.open(url, "_self")