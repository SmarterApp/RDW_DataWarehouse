#globals ok $ EDWARE test require module equals deepEqual
define ["jquery", "edwareBreadcrumbs"], ($, edwareBreadcrumbs) ->

  module "EDWARE.breadcrumbs.create",
    setup: ->
      $("body").append "<div id='breadcrumbs'></div>"

    teardown: ->
      $("#breadcrumbs").remove()

  test "Test create method", ->
    stop()
    create = edwareBreadcrumbs.create
    ok create isnt `undefined`, "edwareBreadcrumbs.create method should be defined"
    ok typeof create is "function", "edwareBreadcrumbs.create method should be function"
    
    breadcrumb = items : [
      type : "state"
      queryParam : "stateCode"
      link : "/assets/html/comparingPopulations.html" 
     ,
      type : "district"
      queryParam : "districtGuid"
      link : "/assets/html/comparingPopulations.html" 
     ,
      type : "school"
      queryParam : "schoolGuid"
      link : "/assets/html/comparingPopulations.html" 
     ,
      type : "grade"
      queryParam : "asmtGrade"
      link : "/assets/html/studentList.html"
     ,
      type : "student"
      queryParam: "student"
    ]
    
    test_data = items: [
      type: "state"
      name: "Washington"
      id: "WA"
    ,
      type: "district"
      name: "Redmond District"
      id: "d1"
    ,
      type: "school"
      name: "Redmond High School"
      id: "s1"
    ,
      type: "grade"
      name: "1"
      id: "1"
    ]
          
    deepEqual $("#breadcrumbs")[0].innerHTML.length, 0, "breadcrumbs should be empty before test is running"
    edwareBreadcrumbs.create("#breadcrumbs", test_data, breadcrumb)
    setTimeout (->
      deepEqual $("#breadcrumbs a").length, 3, "3 links should have been created"
      deepEqual $("#breadcrumbs a")[0].text, "Washington", "wrong text shown"
      start()
    ), 150
    
  test "Test breadcrumb with no links", ->
    stop()
    test_data = items: [
      type: "state"
      name: "Washington"
      id: "WA"
    ]
    
    breadcrumb = items : [
      type : "state"
      queryParam : "stateCode"
      link : "/assets/html/comparingPopulations.html" 
       ,
        type : "district"
      queryParam : "districtGuid"
      link : "/assets/html/comparingPopulations.html" 
      ,
        type : "school"
      queryParam : "schoolGuid"
      link : "/assets/html/comparingPopulations.html" 
      ,
        type : "grade"
      queryParam : "asmtGrade"
      link : "/assets/html/studentList.html"
      ,
        type : "student"
      queryParam: "student"
    ]
    
    edwareBreadcrumbs.create("#breadcrumbs", test_data, breadcrumb)
    setTimeout (->      
      deepEqual $("#breadcrumbs a").length, 0, "0 links should have been created"
      start()
    ), 150
