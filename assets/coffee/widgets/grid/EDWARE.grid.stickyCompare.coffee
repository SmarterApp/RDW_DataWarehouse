define [
  'jquery'
  'mustache'
  'edwareUtil'
  'edwareClientStorage'
  'text!edwareStickyCompareTemplate'
], ($, Mustache, edwareUtil, edwareClientStorage, edwareStickyCompareTemplate) ->
  
  class EdwareGridStickyCompare
   
    constructor: (@labels, @callback) ->
      this.initialize()
      this
      
    initialize: () ->
      this.storage = edwareClientStorage.stickyCompStorage
      this.bindEvents()
      this.createButtonBar()
      this.selectedRows = {}
      this.compareSelectedActions = $('#compareSelectedActions')
      this.compareEnabledActions = $('#compareEnabledActions')
      this.stickyEnabledDescription = $('#stickyEnabledDescription')
      this.stickyCompareBtn = $('#stickyCompare-btn')
      this.stickyChainBtn = $('#stickyChain-btn')
      this.stickyDeselectBtn = $('#stickyDeselect-btn')
      this.stickyShowAllBtn = $('#stickyShowAll-btn')

    # Sets information when we know what type of report it is, etc.
    # compareMode is set to false since we know that the html is reloaded
    setReportInfo: (@reportType, @displayType, @params) ->
      this.compareMode = false
      this.displayType = this.displayType.toLowerCase()
      
    update: () ->
      # Hide buttons based on whether any selection is already made
      # Only perform when compare mode is active
      if this.compareMode
        if this.getRowsCount() > 0
          this.showCompareEnabledButtons()
        else
          this.hideCompareSection()
      else
        # We may reach to this state when user selects some checkbox, and then submit a filter that cause grid to re-render
        if this.getRowsCount() is 0
          this.hideCompareSection()
        else
          # This happens when grid re-renders and we need to reapply selected rows with checkboxes to true and update its text
          for row of this.selectedRows
            element = $('#sticky_' + row)
            element.attr('checked', true)
            this.checkedEvent element
        
    # All events related to grid filtering of rows
    bindEvents: () ->
      self = this  
      # checkboxes in each row
      $(document).on 'click', '.stickyCheckbox', () ->
        if not $(this).is(':checked')
          self.removeCurrentRow this
          self.uncheckedEvent this
        else
          self.addCurrentRow this
          self.checkedEvent this
        self.renderStickyChainRows()
  
      # Binds to compare button in summary row
      $(document).on 'click', '#stickyCompare-btn', () ->
        self.compare()
      
      # Text that appears next to checkbox after checkbox is clicked
      $(document).on 'click', '.stickyCompareLabelChecked', () ->
        self.compare()
      
      # Deselect Button in summary row
      $(document).on 'click', '#stickyDeselect-btn', () ->
        self.clearSelectedRows()
        $('.stickyCheckbox').attr('checked', false)  
        # Remove class of checkedlabel, add class of regular label and then set the text
        label = $('.stickyCheckbox').siblings("label")
        label.toggleClass("stickyCompareLabel stickyCompareLabelChecked")
        label.text(self.labels.compare)
        self.resetCompareRowControls()
      
      # Show all district button
      $(document).on 'click', '#stickyShowAll-btn', () ->
        self.clearSelectedRows()
        self.updateSelection()
      
      # Remove button on each row in grid 
      $(document).on 'click', '.stickyCompareRemove', () ->
        self.removeCurrentRow this
        self.updateSelection()
        
      # Remove Label
      $(document).on 'click', '.stickyRemoveLabel', () ->
        row = $(this).siblings('.stickyCompareRemove')
        self.removeCurrentRow row
        self.updateSelection()
     
      # remove icon on sticky chain
      $(document).on 'click', '.removeStickyChainIcon', () ->
        rowId = $(this).data('id')
        # Uncheck the checkbox in the grid
        element = $('#sticky_' + rowId)
        element.attr('checked', false)
        # We need to explicitly remove the rows
        # because we may run into the case where the row isn't loaded in the grid
        self.removeRowFromSelectedRows rowId
        self.uncheckedEvent element
        self.renderStickyChainRows()
      
      # On logout, clear storage
      $(document).on 'click', '#logout_button', () ->
        # clear session storage
        self.storage.clear()
        
      $(document).on 'click', '.dropdown-menu .stickyChainScrollable', (e)->
        e.stopPropagation();
      
      $(document).on 'mouseenter', '#stickyChain-btn', ()->
        $('#stickyChain-btn').dropdown('toggle')

    clearSelectedRows: () ->
      this.selectedRows = {}
    
    getRows: () ->
      keys = []
      for key, value of this.selectedRows
        keys.push(parseInt(key))
      keys
    
    getRowsCount: () ->
      Object.keys(this.selectedRows).length
      
    # rows have been selected, compare the selections
    compare: () ->
      this.compareMode = true
      this.updateSelection() if this.getRowsCount() > 0
    
    # uncheck of checkbox event
    uncheckedEvent: (element) ->
      label = $(element).siblings("label")
      label.text(this.labels.compare)
      label.toggleClass("stickyCompareLabel stickyCompareLabelChecked")
      
      this.resetCompareRowControls()
    
    # checkbox has been checked
    checkedEvent: (element) ->
      $(element).siblings("label").toggleClass("stickyCompareLabelChecked stickyCompareLabel")
      this.resetCompareRowControls()
              
    # Given a row in the grid, add its value to selectedRows
    addCurrentRow: (row) ->
      info = this.getCurrentRowInfo row
      this.selectedRows[info.id] = info.name
    
    # Given a row in the grid, remove its value from selectedRows
    removeCurrentRow: (row) ->
      info = this.getCurrentRowInfo row
      this.removeRowFromSelectedRows info.id
    
    removeRowFromSelectedRows: (id) ->
      delete this.selectedRows[id]
    
    # Returns the id and name of a row
    getCurrentRowInfo: (row) ->
      {'id': parseInt($(row).data('value')), 'name': $(row).data('name')}
    
    getSelectedRowsFromStorage: () ->
      # When this gets called, it means we should read from storage
      # Set the mode based on whether any rows are returned
      # Gets the rows selected for the current report view
      rows = this.getDataForReport()
      this.selectedRows = {}
      for row in rows
        this.selectedRows[row] = ""
      this.compareMode = rows.length > 0
      this.getRows()
    
    getFilteredInfo: (allData) ->
      # client passes in data and this will return rows that user have selected and whether stickyCompare is enabled
      returnData = []
      selectedRows = this.getSelectedRowsFromStorage()
      if selectedRows.length > 0
        for data in allData
          if returnData.length is selectedRows.length
            break
          if data.rowId in selectedRows
            returnData.push data
      else
        returnData = allData
      return {'data': returnData, 'enabled': selectedRows.length > 0}
    
    getDataForReport: () ->
      # Gets the rows selected for the current report view
      data = this.getDataFromStorage()[this.reportType] || {}
      data[this.getKey()] || []
    
    # Saves to storage
    # Reset compare mode depending on whether any rows are selected
    updateSelection: () ->
      this.saveSelectedRowsToStorage()
      if this.getRowsCount() is 0 and this.compareMode
        this.compareMode = false
        this.hideCompareSection()
      # calls a callback function (render grid)
      this.callback()
    
    # Update session storage for selected rows
    saveSelectedRowsToStorage: () ->
      data = this.getDataFromStorage()
      reportData = data[this.reportType]
      reportData = {} if not reportData
      reportData[this.getKey()] = this.getRows()
      data[this.reportType] = reportData
      this.storage.save data
   
    getDataFromStorage: () ->
      data = JSON.parse(this.storage.load())
      if not data then data = {}
      data
      
    getKey: () ->
      if this.params['schoolGuid'] and this.params['asmtGrade']
        # cache key for los is a combination of schoolguid and asmtGrade
        id = this.params['schoolGuid'] + "_" + this.params['asmtGrade']
      else if this.params['districtGuid']
        id  = this.params['districtGuid']
      else if this.params['stateCode']
        id  = this.params['stateCode']
      id
    
    getDisplayTypes: () ->
      # Returns the plural form of displayType
      this.displayType + "s"
      
    # Reset Grid rows checkbox and button text
    resetCompareRowControls: () ->
      text = this.labels.compare
      labelNameKey = this.displayType
      count = this.getRowsCount()
      if count > 0
        labelNameKey = this.getDisplayTypes() if count > 1
        countText = count + " " + this.labels[labelNameKey]
        this.showCompareSelectedButtons()
      else
        # Hide all buttons
        this.hideCompareSection()
      text += " " + countText if countText
      $('.stickyCheckbox:checked').siblings("label").text(text)
      this.stickyCompareBtn.text(text)
      # To display ex. "districts_selected" label
      this.stickyChainBtn.text(count + " " + this.labels[labelNameKey + "_selected"])
 
    createButtonBar: () ->
      output = Mustache.to_html edwareStickyCompareTemplate, {'labels': this.labels}
      $('#stickyCompareSection').html output
      this.compareSection = $('#stickyCompareSection')
      this.hideCompareSection()
   
    hideCompareSection: () ->
      this.compareSection.hide()
    
    showCompareSection: () ->
      this.compareSection.show()

    showCompareSelectedButtons: () ->
      this.showCompareSection()
      this.compareSelectedActions.show()
      this.compareEnabledActions.hide()
    
    showCompareEnabledButtons: () ->
      this.showCompareSection()
      this.stickyShowAllBtn.text(this.labels.show_all + " " + this.labels[this.getDisplayTypes()])
      count = this.getRowsCount()
      text = this.labels.viewing + " " + String(count) + " " 
      if count > 1 then text += this.labels[this.getDisplayTypes()] else text += this.labels[this.displayType]
      this.stickyEnabledDescription.text(text)
      this.compareSelectedActions.hide()
      this.compareEnabledActions.show()

    renderStickyChainRows: () ->
      element = $('#stickyChainSelectedList')
      element.empty()
      reverse = {}
      for key, value of this.selectedRows
        reverse[value] = key
        
      names = Object.keys(reverse).sort()
      idx = 0
      scrollable =$('<div class="stickyChainScrollable"></div>')
      table = $('<div class=" stickyChainTable"></div>')
      for name in names
        table.append $('<div class="tableRow"><hr class="tableCellHR"/><hr class="tableCellHR"/></div>') if idx > 0
        table.append $('<div class="tableRow"><div class="tableCellLeft">' + name + '</div><div data-id="' + reverse[name] + '" data-name="' + name + '" class="tableCellRight removeStickyChainIcon"></div></div>')
        idx++
      scrollable.append table
      element.append scrollable
      
  EdwareGridStickyCompare:EdwareGridStickyCompare