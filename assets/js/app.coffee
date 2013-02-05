#global define
define ["jquery", "cs!edwareStudentList"], ($, edwareStudentList) ->
    
  #
  #    * Initialize the app
  #    
  initialize = ->
    $(document).ready ->
      
      # This is temporary method until we know which initial page will be displayed
      edwareStudentList.createStudentGrid()

  initialize: initialize
