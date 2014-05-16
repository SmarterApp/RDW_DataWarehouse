define ["jquery"], ($) ->

  $('body').on
    keypress: () ->
      $this = $(this)
      if not $this.hasClass('highlight')
        $this.addClass('highlight')
    mouseup: () ->
      $this = $(this)
      if $this.hasClass('highlight')
        $this.removeClass('highlight')

  # define namespace
  EDWARE = EDWARE or {}

  EDWARE
