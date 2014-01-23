define ["jquery"], ($) ->

  DEFAULT_CONFIG =
    html: true
    trigger: 'hover'
    placement: 'bottom'

  resizePopover = ()->
    offset = $(this).offset().top
    height = window.innerHeight - offset - 100 # add 100px for popover margin
    $(".edwareScrollable").css('max-height', height + 'px')

  $.fn.edwarePopover = (config) ->
    # setup default template with customized class name
    config.template ?= "<div class='popover #{config.class} edwarePopover'><div class='mask'/><div class='arrow'/><div class='popover-content edwareScrollable'><p></p></div></div>"
    config.container ?= this
    config = $.extend({}, DEFAULT_CONFIG, config)
    this.popover config
    self = this
    this.on 'shown.bs.popover', ->
      resizePopover.call(self)
    this.unbind('mouseleave').mouseleave ->
      self.popover 'hide'
    this
