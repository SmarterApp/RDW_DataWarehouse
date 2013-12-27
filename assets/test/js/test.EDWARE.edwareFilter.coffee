#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "edwareFilter"], ($, edwareFilter) ->

  filterConfig =
  	"not_stated_message": "{{percentage}}% reported \"not stated\"",
  	"grades" :
  		"display" : "Grades",
  		"tag" : "Grades",
  		"name" : "grade",
  		"options" : [
        "label" : "Grade 3",
  		 	"value" : "3"
    	,
 				"label" : "Grade 4",
 				"value" : "4"
  		,
 				"label" : "Grade 5",
 				"value" : "5"
  		,
 				"label" : "Grade 6",
 				"value" : "6"
  		,
 				"label" : "Grade 7",
 				"value" : "7"
  		,
 				"label" : "Grade 8",
 				"value" : "8"
  		,
 				"label" : "Grade 11",
 				"value" : "11"
  		]
  	,
  	"filters" : [
        "display" : "Limited English Proficient (LEP)*",
        "tag" : "LEP",
        "name" : "dmgPrgLep",
        "comment" : "*This category includes English Language Learners(ELL) if your state identifies students as ELL",
        "options" : [
          "label": "Yes",
          "value": "Y"
          ,
          "label": "No",
          "value": "N"
          ,
          "label": "Not Stated",
          "value": "NS"
        ]
      ,
        "display" : "Ethnicity",
        "tag" : "Ethnicity",
        "name" : "ethnicity",
        "comment" : "*Not Hispanic or Latino",
        "options" : [
          "label": "Hispanic or Latino (all races)",
          "value": "3"
          ,
          "label": "Black*",
          "value": "1"
          ,
          "label": "Asian*",
          "value": "2"
          ,
          "label": "White*",
          "value": "6"
          ,
          "label": "American Indian or Alaska Native*",
          "value": "4"
          ,
          "label": "Native Hawaiian or Pacific Islander*",
          "value": "5"
          ,
          "label": "Two or more races*",
          "value": "7"
          ,
          "label": "Not Stated",
          "value": "0"
        ]
      ,
        "display" : "IEP",
        "tag" : "IEP",
        "name" : "dmgPrgIep",
        "comment": "*IEP categorization does not include students with a GIEP (i.e., 'gifted' students)",
        "options" : [
          "label": "Yes",
          "value": "Y"
          ,
          "label": "No",
          "value": "N"
          ,
          "label": "Not Stated",
          "value": "NS"
        ]
  		,
        "display" : "Gender",
        "tag" : "Gender",
        "name" : "gender",
        "options" : [
          "label": "Male",
          "value": "male"
          ,
          "label": "Female",
          "value": "female"
          ,
          "label": "Not Stated",
          "value": "not_stated"
        ]
      ,
        "display" : "504",
        "tag" : "504",
        "name" : "dmgPrg504",
        "options" : [
          "label" : "Yes",
          "value" : "Y"
          ,
          "label" : "No",
          "value" : "N"
          ,
          "label": "Not Stated",
          "value": "NS"
        ]
      ]


  module "EDWARE.filter.create",
    setup: ->
      $("body").append "<div id='filterBtn'>Filter Trigger</div><div id='edwareFilter'></div>"

    teardown: ->
      $("#filterBtn").remove()
      $("#edwareFilter").remove()
      
  test "Test jQuery edwareFilter method", ->
    ok $.fn.edwareFilter isnt "undefined", "createFilter method should be defined"
    ok typeof $.fn.edwareFilter is "function", "createFilter method should be function"

  test "Test create method", ->
    filterArea = $('#edwareFilter')
    filterBtn = $('#filterBtn')
    callback = ->
      
    filterArea.edwareFilter filterBtn, filterConfig, callback
    # assertions
    ok not $(filterArea).is(":empty"), "$.fn.edwareFilter function should create filter slide down div"
    notEqual $(filterBtn).find('.filter'), undefined, "filter area should not be empty"
    equal $(filterArea).find('.filter-group').length, 6, "there should be 6 filters in total"
    equal $(filterArea).find('.grade_range input').length, 7, "should be 7 grades' checkbox" 
