define [
  "jquery"
  "mustache"
  "edwarePreferences"
], ($, Mustache, edwarePreferences) ->
  
  DISCLAIMER_TEMPLATE =  
    '<div class="interimDisclaimerIcon">' +
      '<div class="interimDisclaimer hide">{{{content}}}</div>' +
    '</div>'

  DISCLAIMER_POPOVER_TEMPLATE = '<div class="popover interimDisclaimerPopover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"><p></p></div></div></div>'
  
  class EdwareDisclaimer
    
    constructor: (@disclaimerSection, @content) ->
      this.bindEvents()
      this
      
    bindEvents: () ->
      self = this
      # Show tooltip on mouseover
      $(document).on 'mouseenter', '.interimDisclaimerIcon', (e) ->
          e = $(this)
          e.popover
            placement: "bottom"
            trigger: "hover"
            template: DISCLAIMER_POPOVER_TEMPLATE
            content: ->
              e.find(".interimDisclaimer").html() 
          .popover("show")

      # Hide tooltip when click
      $(document).on 'click', '.interimDisclaimerPopover', () ->
        $(this).fadeOut(150)

    # Call this to create the disclaimer icon
    create: () ->
      output = Mustache.to_html DISCLAIMER_TEMPLATE, {'content': this.content}
      this.disclaimerSection.html output
      if not this.hasLoaded()
        # make popup and make it stay
        $('.interimDisclaimerIcon').mouseenter()
        setTimeout ()->
          $('.interimDisclaimerPopover').fadeOut(150)
        , 3000
        # This will save that we've loaded it the first time
        this.saveLoadedInfo()
   
    hasLoaded: () ->
      edwarePreferences.getInterimInfo()
    
    saveLoadedInfo: () ->
      edwarePreferences.saveInterimInfo()
    
    update: (asmtType) ->
      visible = if asmtType is "Comprehensive Interim" then "visible" else "hidden"
      this.disclaimerSection.css('visibility', visible)
        
  (($)->
    $.fn.edwareDisclaimer = (content) ->
      new EdwareDisclaimer($(this), content)
  ) jQuery
