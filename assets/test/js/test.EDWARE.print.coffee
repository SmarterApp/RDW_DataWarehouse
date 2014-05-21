define ["jquery", "edwarePrint", "edwarePreferences"],
($, edwarePrint, edwarePreferences) ->

  PrintModal = edwarePrint.PrintModal
  create = edwarePrint.create

  backupWindowOpenHandler = window.open

  module "EDWARE.Print",
    setup: ->
      edwarePreferences.saveAsmtPreference({"asmtType": "SUMMATIVE"})
      $("body").append "<div id='printModalContainer'></div>"
      # mock window.open function
      window.open = (url)->
        'Mocked url'

    teardown: ->
      edwarePreferences.clearAsmtPreference()
      $('#printModalContainer').remove()
      window.open = backupWindowOpenHandler

  test "Test PrintModal class", ->
    ok PrintModal, "should have a PrintModal class"
    equal typeof(PrintModal), "function", "PrintModal should be a class"
    ok typeof(create), "function", "Print widget should provide a create function"

  test "Test show function", ->
    printModal = create '#printModalContainer', {}
    printModal.show()
    ok $('.modal-backdrop')[0], 'Showing print modal should set up a backdrop'

  test "Test color print function", ->
    printModal = create '#printModalContainer', {}
    actual = printModal.print()
    equal actual, 'Mocked url', 'Should return pdf generating url'
