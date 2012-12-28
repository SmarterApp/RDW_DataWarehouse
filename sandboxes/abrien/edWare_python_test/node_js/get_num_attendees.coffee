fs = require 'fs'
http = require 'http'

source_file = 'myfile'
file_contents = 'File not read yet'

read_source_file = ->
  fs.readFile source_file, 'utf-8', (error, data) ->
    if error
      console.log error
    else
      file_contents = data

fs.watchFile source_file, read_source_file

server = http.createServer (request, response) ->
  response.end file_contents

server.listen 8080, '127.0.0.1'

