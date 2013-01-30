define [
  'jquerySimpleModal'
], ($2) ->
  
  $2(document).ready ->
  "use strict"
  
  $2("#simpleModalButton").click ->
    $2("#simpleModal").modal()
  