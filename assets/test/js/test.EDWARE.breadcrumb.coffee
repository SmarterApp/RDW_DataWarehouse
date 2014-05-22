#globals ok $ EDWARE test require module equals deepEqual
define ["jquery", "edwareBreadcrumbs"], ($, edwareBreadcrumbs) ->

  EdwareBreadcrumbs = edwareBreadcrumbs.EdwareBreadcrumbs

  module "EDWARE.breadcrumbs.create",
    setup: ->
      $("body").append "<div id='breadcrumbs'></div>"

    teardown: ->
      $("#breadcrumbs").remove()

  test "Test create method", ->
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
    edwareBreadcrumbs.create("#breadcrumbs", test_data, breadcrumb, 'home', {})
    equal $("#breadcrumbs a").length, 4, "3 links should have been created"
    equal $("#breadcrumbs a")[0].text, "Washington", "wrong text shown"

  test "Test format name", ->
    EdwareBreadcrumbs::labels = {grade: 'Grade'}
    element = { type: 'grade', name: '1'}
    actual = EdwareBreadcrumbs::formatName element
    equal 'Grade 1', actual.name, "grade name should have grade as prefix"
    element = { type: 'student', name: 'Daniel'}
    actual = EdwareBreadcrumbs::formatName element
    equal "Daniel's Results", actual.name, "student's name should have 's Results as suffix"
    element = { type: 'student', name: 'Daniels'}
    actual = EdwareBreadcrumbs::formatName element
    equal "Daniels' Results", actual.name, "student's name should have 's Results as suffix"
