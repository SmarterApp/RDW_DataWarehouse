define ["jquery"], ($) ->

  lastFocus = undefined

  $.fn.edwareModal = (options) ->
    # flag to indicate whether current modal resets last focused
    # element in the page
    resetLastFocus = true unless options?.keepLastFocus
    # bind events when initialize
    if not options or typeof(options) is 'object'
      # remember last focus
      this.on 'show', ->
        lastFocus = document.activeElement if resetLastFocus
      # restore last focus
      this.on 'hidden', ->
        lastFocus.focus() if lastFocus
    this.modal options
