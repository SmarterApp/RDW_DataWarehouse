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

    $body = $('body')
    bodyLeft = $body.offset().left
    bodyRight = bodyLeft + $body.width()
    popLeft = bodyLeft - popLeft + 20

    $popover.css "left", "+=#{popLeft}"

    arrowLeft = $popover.width() / 2 - popLeft
    $(".arrow", $popover).css "left", arrowLeft



    # update arrow
    # arrow =
    # arrow.css "left", offset - popoverOffset + $(this).width() / 2

  $.fn.edwarePopover = (config) ->
    # setup default template with customized class name
    config.template ?= "<div class='popover #{config.class} edwarePopover'><div class='mask'/><div class='arrow'/><div class='popover-content edwareScrollable'><p></p></div></div>"
    config.container ?= this
    config = $.extend({}, DEFAULT_CONFIG, config)
    this.popover config
    self = this
    this.on 'shown.bs.popover', ->
      reposition.call(self)
      resize.call(self)
    this.unbind('mouseleave').mouseleave ->
      self.popover 'hide'
    this
