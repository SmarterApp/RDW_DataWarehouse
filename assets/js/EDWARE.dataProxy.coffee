#global define
define ["jquery"], ($) ->
  
  #
  #    * Get Student data from the server
  #    * @param sourceURL - The student data API call
  #    * @param callback - callback function
  #    
  getStudentData = (sourceURL, callback) ->
    return false  if sourceURL is "undefined" or typeof sourceURL is "number" or typeof sourceURL is "function" or typeof sourceURL is "object"
      
    assessment_query_params =
      districtId: 4
      schoolId: 3
      asmtGrade: "1" 
    
    $.ajax(
      type: "POST"
      url: sourceURL
      data:
        JSON.stringify(assessment_query_params);
      dataType: "json"
      contentType: "application/json"
    ).done (data) ->
      assessmentsData = data.assessments
      assessmentCutpoints = data.cutpoints
      
      if callback
        callback assessmentsData, assessmentCutpoints
      else
        assessmentArray = [assessmentsData, assessmentCutpoints]

  #
  #    * Get student list columns configuration
  # 
  getStudentsConfig = (studentColumnCfgs, callback) ->
      return false  if studentColumnCfgs is "undefined" or typeof studentColumnCfgs is "number" or typeof studentColumnCfgs is "function" or typeof studentColumnCfgs is "object"
        
      $.getJSON studentColumnCfgs, (data) ->
        studentsConfig = data.students
        
        if callback
           callback studentsConfig
        else
           studentsConfig
         
      
  getStudentData: getStudentData
  getStudentsConfig: getStudentsConfig