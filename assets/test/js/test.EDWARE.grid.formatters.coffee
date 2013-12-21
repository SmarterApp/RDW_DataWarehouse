#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "jqGrid", "edwareGridFormatters"], ($, jqGrid, edwareGridFormatters) ->
  module "EDWARE.grid.formatters",

  test "Test totalPopulation Formatter", ->
    equal typeof(edwareGridFormatters.totalPopulation), "function", "Function Exists"
    value = 35
    options = JSON.parse '{"colModel": {"export": "true", "formatoptions" : {"asmt_type": "subject1"}, "labels": {"insufficient_data": "ut", "total_assessed": "t", "filtered_student_count": "c", "filtered_percentage_of_total": "d"}}}'   
    rowObject = JSON.parse '{"id": "242", "name": "test", "results": {"subject1": {"asmt_subject": "Math","total": 35,"sortedValue": 60,"leftTotalPercentage": 60,"rightTotalPercentage": 40,"export": "edwareExportColumn","alignment": 11.45,"alignmentLine": 104.45}}}'

    val = edwareGridFormatters.totalPopulation value, options, rowObject
    obj = $(val)
    equal obj.find(".studentsTotal").size(), 1, "Student Total Found"
    equal obj.find(".edwareExportField").size(), 1, "Export Field Found"

  test "Test totalPopulation Formatter with Filtering on", ->
      value = 35
      options = JSON.parse '{"colModel": {"export": "true", "formatoptions" : {"asmt_type": "subject1"}, "labels": {"insufficient_data": "ut", "total_assessed": "t", "filtered_student_count": "c", "filtered_percentage_of_total": "d"}}}'   
      rowObject = JSON.parse '{"id": "242", "name": "test", "results": {"subject1": {"asmt_subject": "Math","total": 35,"unfilteredTotal": 23,"sortedValue": 60,"leftTotalPercentage": 60,"rightTotalPercentage": 40,"export": "edwareExportColumn","alignment": 11.45,"alignmentLine": 104.45}}}'
  
      val = edwareGridFormatters.totalPopulation value, options, rowObject
      obj = $(val)
      equal obj.find(".studentsTotal").size(), 1, "Student Total Found"
      equal obj.find(".edwareExportField").size(), 3, "Export Field Found"
      equal obj.find(".unfilteredTotal").size(), 1, "Unfiltered Field Found"
      
  test "Test totalPopulation Formatter with Insufficient Data and Filtering", ->
      value = 35
      options = JSON.parse '{"colModel": {"export": "true", "formatoptions" : {"asmt_type": "subject1"}, "labels": {"insufficient_data": "ut", "total_assessed": "t", "filtered_student_count": "c", "filtered_percentage_of_total": "d"}}}'   
      rowObject = JSON.parse '{"id": "242", "name": "test", "results": {"subject1": {"asmt_subject": "Math","total": -1,"unfilteredTotal": 23,"sortedValue": 60,"leftTotalPercentage": 60,"rightTotalPercentage": 40,"export": "edwareExportColumn","alignment": 11.45,"alignmentLine": 104.45}}}'
  
      val = edwareGridFormatters.totalPopulation value, options, rowObject
      obj = $(val)
      equal obj.find(".studentsTotal").size(), 0, "Student Total is Non-zero"
      equal obj.find(".edwareExportField").size(), 3, "Export Field Found"
      equal obj.find(".unfilteredTotal").size(), 0, "UnfilteredTotal is Non-Zero"

  test "Test totalPopulation Formatter with Insufficient Data", ->
      value = 35
      options = JSON.parse '{"colModel": {"export": "true", "formatoptions" : {"asmt_type": "subject1"}, "labels": {"insufficient_data": "ut", "total_assessed": "t", "filtered_student_count": "c", "filtered_percentage_of_total": "d"}}}'   
      rowObject = JSON.parse '{"id": "242", "name": "test", "results": {"subject1": {"asmt_subject": "Math","total": -1,"sortedValue": 60,"leftTotalPercentage": 60,"rightTotalPercentage": 40,"export": "edwareExportColumn","alignment": 11.45,"alignmentLine": 104.45}}}'
  
      val = edwareGridFormatters.totalPopulation value, options, rowObject
      obj = $(val)
      equal obj.find(".studentsTotal").size(), 0, "Student Total is Non-zero"
      equal obj.find(".edwareExportField").size(), 1, "Export Field Found"
      equal obj.find(".unfilteredTotal").size(), 0, "UnfilteredTotal is Non-Zero"
 
  test "Test populationBar Formatter", ->
    equal typeof(edwareGridFormatters.populationBar), "function", "Function Exists"
