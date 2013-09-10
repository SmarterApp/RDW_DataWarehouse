define [
  "jquery"
  "mustache"
  "text!edwareDropdownTemplate"
], ($, Mustache, dropdownTemplate) ->

  # create dropdown menu for color bars
  class EdwareDropdownMenu
    
    constructor: (@dropdown, @config, @callback) ->
      this.menu = this.create()
      this.arrows = $('.arrow', this.menu)
      this.bindEvents()
      return this.menu
    
    bindEvents: () ->
      self = this;
      $('input.inputColorBlock', this.menu).click (e) ->
        e.stopPropagation()        
        self.dropdown.resetAll()
        self.sort e.target

      $('ul', this.menu).click (e)->
        e.stopPropagation()
        $(e.target).closest('.center').removeClass('open')

    sort: (sortItem) ->
      $this = $(sortItem)
      # check current selection
      $this.attr('checked', true)
      # check current selection
      dropdown = $this.closest('div.dropdown').addClass('active')
      # obtain selected color bar and set it to table header
      colorBar = $this.next().clone()
      # set the center of table header
      $('.dropdown_title', dropdown).html(colorBar)
      # set center
      $('.center', dropdown).width $this.data('width')
      # show arrow
      this.arrows.toggleClass('hide');
      subject = dropdown.data('subject')
      index = $this.data('index')
      this.dropdown.callback {name: subject, index: index, order: 'asc'}

    create: () ->
      # create dropdown and set to the center of each colomn
      output = $(Mustache.to_html dropdownTemplate, this.config)
      # remove the last color bar
      output.find('li:nth-last-child(2)').remove()
      # set margin for color bar
      options = output.find('li')
      $.each options, (index, element) ->
        $('.colorBlock', element).eq(index).addClass('margin_right')
        # set index for sorting
        $('input', element).attr('data-index', index)
      output

  class EdwareDropdown
    
    constructor: (@dropdownSection, @customALDDropdown, @callback) ->
      this.menus = {}
      this.bindEvents()
      
    update: (@summaryData, @asmtSubjectsData, @colorsData) ->
      # Hide the drop down if data is empty
      this.hideEmptyData()
      this.create()

    bindEvents: () ->
      $(document).on 'click', '.dropdown.active', (e) ->
        $this = $(this)
        sortBtn = $("#" + $this.data('subject') + "_sort")
        $('.arrow', $this).toggleClass('desc');
        sortBtn.trigger 'click'
        
    hideEmptyData: () ->
      for subject, asmtSubject of this.asmtSubjectsData
        if not this.hasData(subject) and this.hasMenu(subject)
          $(this.menus[subject]).remove()
          this.menus[subject] = undefined
    
    create: () ->
      for subject in Object.keys(this.asmtSubjectsData).sort()
        asmtSubject = this.asmtSubjectsData[subject]
        if this.hasSubject(subject) and not this.hasMenu(subject) and this.hasData(subject)
          config = this.generateConfig(subject, asmtSubject)
          menu = new EdwareDropdownMenu(this, config)
          #cache generated dropdown menu
          this.menus[subject] = menu
          $(this.dropdownSection).append menu
          
    hasData: (subject) ->
      this.summaryData.results and this.summaryData.results[subject] and this.summaryData.results[subject].total != -1

    hasSubject: (subject) ->
      this.colorsData[subject] isnt undefined
     
    hasMenu: (subject) ->
      this.menus[subject] isnt undefined

    generateConfig: (subject, asmtSubject) ->
      this.config = {}
      this.config['totalStudents'] = this.customALDDropdown.totalStudents
      this.config['selectSort'] = this.customALDDropdown.selectSort
      this.config['colors'] = this.colorsData[subject].colors
      this.config['asmtSubject'] = asmtSubject
      this.config
          
    resetAll: () ->
      # unselect radio button
      $('.inputColorBlock').attr('checked', false)
      $dropdown = $('.dropdown')
      $dropdown.removeClass('active').unbind('click')
      $('.center', $dropdown).removeClass('open').attr('style','')
      # hide arrow icons
      $(".arrow", $dropdown).addClass('hide')
      $('.dropdown_title').html this.config['selectSort'] if this.config isnt undefined


  #
  #    *  EDWARE Filter plugin
  #    *  @param filterHook - Panel config data
  #    *  @param filterTrigger - 
  #    *  @param callback - callback function, triggered by click event on apply button
  #    *  Example: $("#table1").edwareFilter(filterTrigger, callbackFunction)
  #  
  (($)->
    $.fn.edwareDropdown = (customALDDropdown, callback) ->
      new EdwareDropdown($(this), customALDDropdown, callback)
  ) jQuery
