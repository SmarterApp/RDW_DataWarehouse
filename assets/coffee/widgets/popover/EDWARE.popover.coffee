define ["jquery", "edwareEvents"], ($, edwareEvents) ->

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
    popTop = $popover.offset().top
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
    
    # Reposition the mask according to whether popover is placed on top or bottom
    arrowTop = $(".arrow", $popover).offset().top
    maskTop = if arrowTop < popTop then -15 else $popover.height() - 7
    $(".mask", $popover).css "top", maskTop

  $(document).keyup (e)->
    if e.keyCode is 27
      $('.popover').parent().popover 'hide'

  $.fn.edwarePopover = (config) ->
    # default tabindex
    config.tabindex = -1 if config.tabindex is undefined
    config.id = config.class if not config.id
    # setup default template with customized class name
    if config.labelledby
      config.template ?= "<div id='#{config.id}' aria-labelledby='#{config.labelledby}' class='popover #{config.class} edwarePopover'>"
    else
      config.template ?= "<div id='#{config.id}' class='popover #{config.class} edwarePopover'>"
    config.template += "<div class='mask'/><div class='arrow'/>
      <div class='popover-content edwareScrollable' tabindex='#{config.tabindex}'><p></p></div></div>"
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

  createPopover = (config) ->
    # Creates popovers for multiple items on a page given that the content is embedded in the parent node
    $(config.source).each ->
      $(this).edwarePopover
        class: config.target
        content: $(this).parent().find(config.contentContainer).html()
        container: $(config.container) if config.container
        tabindex: if config.tabindex else 0
        placement: if config.placement else 'top'
    .click ->
      $(this).mouseover()
  
  createPopover:createPopover