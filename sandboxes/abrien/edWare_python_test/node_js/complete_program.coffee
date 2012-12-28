fs = require 'fs'
http = require 'http'
coffee = require 'coffee-script'

attendees = 0
friends = 0

split = (text) ->
  text.split /,/g

accumulate = (initial, numbers, accumulator) ->
  total = initial or 0
  for number in numbers
    total = accumulator total, number
  total

sum = (accum, current) -> accum + current

attendees_counter = (data) ->
  attendees = data.split(/,/).length

friends_counter = (data) ->
  numbers = (parseInt(string) for string in split data)
  friends = accumulate(0, numbers, sum)

read_file = (file, strategy) ->
  fs.readFile file, 'utf-8', (error, response) ->
    throw error if error
    strategy response

count_using_file = (file, strategy) ->
  read_file file, strategy
  fs.watchFile file, (-> read_file file, strategy)

count_using_file 'partygoers.txt', attendees_counter
count_using_file 'friends.txt', friends_counter

server = http.createServer (request, response) ->
  switch request.url
    when '/'
      response.writeHead 200, 'Content-Type': 'text/html'
      response.end view
    when '/count'
      response.writeHead 200, 'Content-Type': 'text/plain'
      response.end "#{attendees + friends}"

server.listen 8080, '127.0.0.1'

client_script = coffee.compile '''
showAttendees = ->
  $.get "/count", (response) ->
    $("#how-many-attendees").html("#{response} attendees!")
showAttendees()
setInterval showAttendees, 1000 '''

view = """
<!doctype html>
<title>How many people are coming?</title>
<body>
<div id='how-many-attendees'></div>
<script src='http://code.jquery.com/jquery-1.6.2.js'></script> #11 <script> #11 #{client_script} #11 </script> #11 """