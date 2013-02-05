#global define
define ["jquery", "cs!edwareDataProxy", "cs!edwareGrid"], ($, edwareDataProxy, edwareGrid) ->
  
  assessmentCutpoints = {}
      
  #
  #    * Create Student data grid
  #    
      
  createStudentGrid = ->
      
    edwareDataProxy.getStudentData "/data/list_of_students", (assessmentsData, assessmentCutpoints) ->
      
      edwareDataProxy.getStudentsConfig "../data/student.json", (studentsConfig) ->
        edwareGrid.create "gridTable", studentsConfig, assessmentsData, assessmentCutpoints
    
  #
  #    * Initialize the app
  #    
  initialize = ->
    $(document).ready ->
      createStudentGrid()

  initialize: initialize
