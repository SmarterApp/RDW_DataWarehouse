define [
  "jquery"
  "mustache"
  "edwarePreferences"
], ($, Mustache, edwarePreferences) ->
  
  DISCLAIMER_TEMPLATE =  
    '<div class="interimDisclaimerIcon">' +
      '<div class="interimDisclaimer hide">{{{content}}}</div>' +
    '</div>'
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
            html: true
            placement: "bottom"
            trigger: "manual"
            template: '<div class="popover interimDisclaimerPopover"><div class="arrow"></div><div class="popover-inner"><div class="popover-content"><p></p></div></div></div>'
            content: ->
              e.find(".interimDisclaimer").html() 
          .popover("show")
      $(document).on 'click', '.interimDisclaimerIcon', (e) ->
          e.preventDefault()
      $(document).on 'mouseleave', '.interimDisclaimerIcon', (e) ->
          e = $(this)
          e.popover("hide")

    # Call this to create the disclaimer icon
    create: () ->
      output = Mustache.to_html DISCLAIMER_TEMPLATE, {'content': this.content}
      this.disclaimerSection.html output
      if not this.hasLoaded()
        # TODO make popup and make it stay
        
        # This will save that we've loaded it the first time
        this.saveLoadedInfo()
   
    hasLoaded: () ->
      edwarePreferences.getInterimInfo()
    
    saveLoadedInfo: () ->
      edwarePreferences.saveInterimInfo()
        
  (($)->
    $.fn.edwareDisclaimer = (content) ->
      new EdwareDisclaimer($(this), content)
  ) jQuery
