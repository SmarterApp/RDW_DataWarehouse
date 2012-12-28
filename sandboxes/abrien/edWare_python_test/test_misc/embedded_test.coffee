even = (number) ->
    not (number%2)

evens = (range) ->
  num for num in range when even num

console.log evens [1..100]