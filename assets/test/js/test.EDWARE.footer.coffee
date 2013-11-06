#globals ok $ EDWARE test require module equals deepEqual
define ["jquery", "edwareFooter"], ($, edwareFooter) ->

  module "EDWARE.footer",
    setup: ->
      $("body").append "<div id='footer'></div>"
      
    teardown: ->
      $("#footer").remove()


  test "Test EdwareFooter class", ->
    edwareFooter = edwareFooter.EdwareFooter
    ok edwareFooter isnt 'undefined', "EdwareFooter should be defined"
    ok typeof edwareFooter is 'function', "EdwareFooter should be a function class"


  # test "Test export menu", ->
  #   $.getJSON "resources/FooterConfig.json", (data) ->
  #     console.log data
  #     new edwareFooter.EdwareFooter("comparing_populations", data, "state")
  #   $("a#export").trigger 'click'
  #   equal $("input:radio[name='export_button']").length, 1, "Export menu should contain export to csv option"
    
