define ["jquery"], ($) ->

  DEFAULT_CONFIG =
    html: true
    trigger: 'hover'
    placement: 'bottom'

  resize = ()->
    offset = $(this).offset().top
    height = window.innerHeight - offset - 100 # add 100px for popover margin
    $(".edwareScrollable").css('max-height', height + 'px')

  reposition = () ->
    # center legend popover to prevent it overflow the screen
    $popover = $('.edwarePopover')
    popLeft = $popover.offset().left
    popRight = popLeft + $popover.width()

    $body = $('#header') # use header element to make sure offset left consistant cross browsers
    bodyLeft = $body.offset().left
    bodyRight = bodyLeft + $body.width()

    if popLeft < bodyLeft
      popLeft = bodyLeft - popLeft + 20
      $popover.css "left", "+=#{popLeft}"
      arrowLeft = $popover.width() / 2 - popLeft
      $(".arrow", $popover).css "left", arrowLeft

    if popRight > bodyRight
      popRight = popRight - bodyRight + 20
      $popover.css "left", "-=#{popRight}"
      arrowLeft = $popover.width() / 2 + popRight
      $(".arrow", $popover).css "left", arrowLeft

  $(document).keyup (e)->
    if e.keyCode is 27
      $('.popover').parent().popover 'hide'

  $.fn.edwarePopover = (config) ->
    # setup default template with customized class name
    config.template ?= "<div class='popover #{config.class} edwarePopover'><div class='mask'/><div class='arrow'/><div class='popover-content edwareScrollable' tabindex='0'><p></p></div></div>"
    config.container ?= this
    config = $.extend({}, DEFAULT_CONFIG, config)
    this.popover config
    self = this
    this.on 'shown.bs.popover', ->
      reposition.call(self)
      resize.call(self)
      # hide popover when focus out
      self.focuslost ->
        self.popover 'hide'
    this.unbind('mouseleave').on 'mouseleave', ->
      self.popover 'hide'
    this
