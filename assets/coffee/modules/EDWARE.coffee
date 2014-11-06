define ["jquery"], ($) ->

  # define namespace
  # TODO: we don't use this object from the beginning, maybe we should start using it
  EDWARE = EDWARE or {}

  EDWARE

  # bug from wkhtmltopdf causes issue when we use bind https://github.com/masayuki0812/c3/issues/552
  Function::bind = Function::bind or (thisp) ->
    fn = this
    ->
      fn.apply thisp, arguments
