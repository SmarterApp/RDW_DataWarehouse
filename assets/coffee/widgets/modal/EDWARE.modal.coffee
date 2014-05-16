define ["jquery"], ($) ->

  lastFocus = undefined

  $.fn.edwareModal = (options) ->
    # bind events when initialize
    if not options or typeof(options) is 'object'
      # remember last focus
      this.on 'show', ->
        lastFocus = document.activeElement
      # restore last focus
      this.on 'hidden', ->
        lastFocus.focus() if lastFocus
    this.modal options
