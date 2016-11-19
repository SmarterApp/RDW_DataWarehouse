#globals ok $ EDWARE test require module equals deepEqual
require ["jquery", "edwareUtil"], ($, edwareUtil) ->
  module "EDWARE.util",
    setup: ->
      $("body").append "<div id=errorMessage></div>"

    teardown: ->
      $("#errorMessage").remove()

  test "displayErrorMessage", ->
    ok edwareUtil.displayErrorMessage isnt `undefined`, "EDWARE.util displayErrorMessage method should be defined"
    ok typeof edwareUtil.displayErrorMessage is "function", "EDWARE.util displayErrorMessage method should be function"
    
    edwareUtil.displayErrorMessage "Error found"
    deepEqual $("#errorMessage").html(), "Error found", "Error displayed on the page"

  test 'deepCopy', ->
    ok edwareUtil.deepCopy isnt 'undefined', 'should be defined'
    ok typeof edwareUtil.deepCopy is 'function', 'should be defined as a function'

    a = {x:{y:[]}}
    b = edwareUtil.deepCopy a
    ok a != b, 'deepCopy() should return unique object'
    ok a.x != b.x, 'deepCopy() should return unique object'
    ok a.x.y != b.x.y, 'deepCopy() should return unique object'

    a = {object:{}, array:[], number: 1, fn: (->
    ), boolean: true, regexp: /a/, date: new Date}
    b = edwareUtil.deepCopy a
    ok b.object instanceof Object, 'should support native type: Object'
    ok b.array instanceof Array, 'should support native type: Array'
    ok b.number is 1, 'should support native type: number'
    ok b.fn instanceof Function, 'should support native type: Function'
    ok b.boolean is true, 'should support native type: booleans'
    ok b.regexp instanceof RegExp, 'should support native type: RegExp'
    ok b.date instanceof Date, 'should support native type: Date'
    ok a.time == b.time, 'should support native type: date'

    raises (->
      edwareUtil.deepCopy {0:{1:{2:{3:{4:{5:{6:{7:{8:{9:{10:{11:{}}}}}}}}}}}}}
      return
    ), Error, 'should not perform infinite recursion.'

