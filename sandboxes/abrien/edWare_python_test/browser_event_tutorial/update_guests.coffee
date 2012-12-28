showGuests = ->
  $.get "attendees.js", (response) ->
    $("#how-many-attendees").html "#{response} attendees!"

setInterval(showGuests, 1000)