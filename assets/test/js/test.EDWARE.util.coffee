#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "cs!sourceJS/EDWARE.util"], ($, edwareUtil) ->
  module "EDWARE.util.displayErrorMessage",
    setup: ->
      $("body").append "<div id=errorMessage></div>"

    teardown: ->
      $("#errorMessage").remove()

  test "Test create method", ->
    ok edwareUtil.displayErrorMessage isnt `undefined`, "EDWARE.util displayErrorMessage method should be defined"
    ok typeof edwareUtil.displayErrorMessage is "function", "EDWARE.util displayErrorMessage method should be function"
    
    edwareUtil.displayErrorMessage "Error found"
    deepEqual $("#errorMessage").html(), "Error found", "Error displayed on the page"
