define [
  "jquery"
  "mustache"
  "bootstrap"
  "edwareDataProxy"
  "edwareUtil"
  "edwareClientStorage"
  "text!edwareFilterTemplate"
  "edwareGrid"
], ($, Mustache, bootstrap, edwareDataProxy, edwareUtil, edwareClientStorage, filterTemplate, edwareGrid) ->

  # * EDWARE filter widget
  # * The module contains EDWARE filter creation method
  FILTER_CLOSE = 'edware.filter.close'

  FILTER_SUBMIT = 'edware.filter.submit'

  RESET_DROPDOWN = 'edware.filter.reset.dropdown'

  class EdwareFilter

    constructor: (@filterArea, @filterTrigger, @configs, @callback) ->
      this.loadPage()
      this.initialize()
      # bind click event
      this.bindEvents()
      return this

    initialize: ->
      # initialize variables
      this.filterArrow = $('.filterArrow', this.filterArea)
      this.filterPanel = $('.filter', this.filterArea)
      this.dropdownMenu = $('.dropdown-menu', this.filterArea)
      this.options = $('input', self.dropdownMenu)
      this.cancelButton = $('#cancel-btn', this.filterArea)
      this.submitButton = $('#submit-btn', this.filterArea)
      this.gradesFilter = $('.grade_range label input', this.filterPanel)
      this.filters = $('.filter-group', this.filterPanel)
      this.tagPanelWrapper = $('.selectedFilter_panel', this.filterArea)
      this.tagPanel = $('.filters', this.tagPanelWrapper)
      this.clearAllButton = $('.removeAllFilters', this.filterArea)
      # set session storage
      this.storage = edwareClientStorage.filterStorage
      this.template = this.configs['not_stated_message']

    loadPage: ->
      # load config from server
      output = Mustache.to_html filterTemplate, this.configs
      $(this.filterArea).html output

    bindEvents: ->
      self = this
      # subscribe filter close event
      this.filterArea.on FILTER_CLOSE, () ->
        self.closeFilter()

      # attach click event to cancel button
      this.cancelButton.click () ->
        self.cancel self

      # attach click event to submit button
      this.submitButton.click () ->
        $(self).trigger FILTER_SUBMIT

      # attach click event to filter trigger button
      $(document).off 'click', this.filterTrigger
      $(document).on 'click', this.filterTrigger, ->
        self.toggleFilterArea self

      # toggle grades checkbox effect
      this.gradesFilter.click () ->
        $(this).parent().toggleClass('blue')

      # prevent dropdown memu from disappearing
      $(this.dropdownMenu).click (e) ->
        e.stopPropagation()

      $(this.filters).on RESET_DROPDOWN, this.clearOptions

      $(this).on FILTER_SUBMIT, self.submitFilter

      # attach click event to 'Clear All' button
      $(this.clearAllButton).click ->
        self.clearAll()

      # display user selected option on dropdown
      $(this.options).click ->
        self.showOptions $(this).closest('.btn-group')

      # bind logout events
      $(document).on 'click', '#logout_button', () ->
        # clear session storage
        self.storage.clear()

      # collapse dropdown menu when focus out
      $('.filter-group-focuslost', this.filterArea).focuslost ()->
        $(this).parent().removeClass('open')

    cancel: (self) ->
      self.reset()
      self.closeFilter()

    reset: () ->
      # reset all filters
      this.filters.each () ->
        $(this).trigger RESET_DROPDOWN
      # load params from session storage
      params = this.storage.load()
      # reset params
      if params
        $.each JSON.parse(params), (key, value) ->
          filter = $('.filter-group[data-name=' + key + ']')
          if filter isnt undefined
            $('input', filter).each ->
              $(this).attr('checked', true).triggerHandler('click') if $(this).val() in value

    toggleFilterArea: (self) ->
      filterPanel = $('.filter', self.filterArea)
      filterArrow = $('.filterArrow')
      if filterPanel.is(':hidden')
         filterArrow.show()
         filterPanel.slideDown 'slow'
         # highlight trigger
         $(this.filterTrigger).addClass('active')
      else
         self.cancel self

    closeFilter: (callback) ->
      this.filterPanel.slideUp 'slow'
      $(this.filterTrigger).removeClass('active')
      $('a', this.filterTrigger).focus()
      noTags = $(this.tagPanel).is(':empty')
      if noTags
        filterArrow = this.filterArrow
        this.tagPanelWrapper.slideUp 'slow', ->
          filterArrow.hide()
          edwareGrid.adjustHeight()
      else
        this.tagPanelWrapper.show()
        this.filterArrow.show()
      callback() if callback

    clearAll: ->
      # clear tag panel
      $(this.tagPanel).html("")
      # reset all filters
      this.filters.each () ->
        $(this).trigger RESET_DROPDOWN
      # trigger ajax call
      $(this).trigger FILTER_SUBMIT

    submitFilter: ->
      self = this
      # display selected filters on html page
      self.createFilterBar self
      self.closeFilter ->
          self.submitAjaxCall self.callback

    createFilterBar: ->
      self = this
      # remove existing filter labels
      this.tagPanel.empty()

      # create tags for selected filter options
      this.filters.each () ->
        tag = new EdwareFilterTag($(this), self)
        $(self.tagPanel).append tag.create() unless tag.isEmpty

    submitAjaxCall: (callback) ->
      selectedValues = this.getSelectedValues()
      # construct params and send ajax call
      params = edwareUtil.getUrlParams()
      # merge selected options into param
      $.extend(params, selectedValues)
      # save param to session storage
      this.storage.save(params)
      callback params if callback

    # get parameters for ajax call
    getSelectedValues: ->
      # get fields of selected options in json format
      params = {}
      $('.filter-group').each () ->
        paramName = $(this).data('name')
        paramValues = []
        $(this).find('input:checked').each () ->
          paramValues.push String($(this).data('value'))
        params[paramName] = paramValues if paramValues.length > 0
      params

    clearOptions: ->
      checkBox = $(this).find("input:checked")
      checkBox.attr("checked", false)
      checkBox.parent().toggleClass('blue')
      # reset dropdown component text
      $(this).find('.selected').remove()

    # show selected options on dropdown component
    showOptions: (buttonGroup) ->
      text = this.getSelectedOptionText buttonGroup
      # remove existing text
      button = $('button', buttonGroup)
      $('.selected', button).remove()
      # compute width property, subtract 20px for margin
      textLength = this.computeTextWidth button
      $('.display', button).append $('<div class="selected">').css('width', textLength).text(text)

    # get selected option text as string separated by comma
    getSelectedOptionText: (buttonGroup) ->
      delimiter = ', '
      text =  $('input:checked', buttonGroup).map(() ->
                    $(this).data('label')
              ).get().join(delimiter)
      if text isnt "" then '[' + text + ']'  else ""

    # compute width property for text
    computeTextWidth: (button) ->
      # compute display text width this way because $().width() doesn't work somehow
      displayWidth = $('.display', button).text().length * 10
      width = $(button).width() - displayWidth - 35
      # keep minimum width 30px
      if width > 0 then width else 30

    loadReport: (params) ->
      this.reset()
      this.submitFilter()

    update: (data) ->
      self = this
      total = data['total']
      $('.filter-wrapper').each () ->
        filterName = $(this).data('name')
        count = data[filterName]
        percentage = Math.round(count * 100.0 / total)
        if percentage > 0
          # show percentage
          self.updatePercentage(this, percentage)
        else
          # hide percentage
          self.hidePercentage(this)

    hidePercentage: (filter) ->
      $('p.not_stated', filter).remove()


    updatePercentage: (filter, percentage) ->
      output = Mustache.to_html this.template, { 'percentage': percentage }
      $('p.not_stated', filter).html output


  class EdwareFilterTag

    constructor: (@dropdown, @filter) ->
      this.init()
      this.bindEvents()

    create: ->
      this.label

    init: ->
      param = {}
      param.display = this.dropdown.data('display')
      param.values = []
      this.dropdown.find('input:checked').each () ->
        label = $(this).data('label').toString()
        # remove asterisk * from the label
        label = label.replace /\*$/, ""
        param.values.push label
      this.label = this.generateLabel param
      this.isEmpty = (param.values.length is 0)

    generateLabel: (data) ->
      template = "<span class='selectedFilterGroup'>
        <span aria-hidden='true' id='aria-{{display}}'>
          <span>{{display}}: </span>
          {{#values}}
            <span>{{.}}</span><span class='seperator'>, </span>
          {{/values}}
        </span>
        <a href='#' class='removeIcon' role='button'
          aria-labelledby='aria-filtered-by aria-{{display}} aria-filter-remove'/>
      </span>"
      output = Mustache.to_html(template, data)
      $(output)

    bindEvents: ->
      self = this
      # attach click event on remove icon
      $('.removeIcon', this.label).click () ->
        self.remove self

    # remove individual filters
    remove: (self) ->
      #remove label
      $(self.label).remove()
      # reset filter
      $(self.dropdown).trigger RESET_DROPDOWN
      # trigger ajax call
      $(self.filter).trigger FILTER_SUBMIT



  filterData = (data, filters) ->
    # no filters applied
    return data if not filters

    match = createFilter(filters)
    for effectiveDate, assessment of data.assessments
      for asmtType, studentList of assessment
        for studentId, assessment of studentList
          if not match.demographics(assessment)
            assessment.hide = true
          else
            assessment.hide = false
          # check grouping filters
          for subject of data.subjects
            asmt_subject = assessment[subject]
            continue if not asmt_subject
            if not match.grouping(asmt_subject)
              asmt_subject.hide = true
            else
              asmt_subject.hide = false
    data

  createFilter = (filters) ->

    return {
      demographics : (assessment) ->
        # TODO: may need refactoring
        for filterName, filterValue of filters
          # do not check other attributes
          if not $.isArray(filterValue)
            continue
          if filterName.substr(0, 5) isnt 'group' # do not check grouping filters
            return false if assessment.demographic[filterName] not in filterValue
        return true

      grouping: (subject) ->
        group_1 = filters.group_1
        group_2 = filters.group_2
        # we take as a match if there's no grouping filter, or current group id is within filters
        in_group_1 = not group_1 or subject.group_1_id in group_1
        in_group_2 = not group_2 or subject.group_2_id in group_2
        return in_group_1 && in_group_2
    }


  #
  #    *  EDWARE Filter plugin
  #    *  @param filterHook - Panel config data
  #    *  @param filterTrigger -
  #    *  @param callback - callback function, triggered by click event on apply button
  #    *  Example: $("#table1").edwareFilter(filterTrigger, callbackFunction)
  #
  (($)->
    $.fn.edwareFilter = (filterTrigger, configs, callback) ->
      new EdwareFilter($(this), filterTrigger, configs, callback)
  ) jQuery

  filterData: filterData
