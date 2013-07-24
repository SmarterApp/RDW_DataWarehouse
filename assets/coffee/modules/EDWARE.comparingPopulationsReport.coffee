require ["../main"], (common) ->
  require ["EDWARE.comparingPopulations", "edwareFilter", "edwareDataProxy"], (edwareComparingPopulations,edwareFilter, edwareDataProxy) ->
	  # Add filter to the page
	  configs = {}
	
	  ( () ->
	    options =
	        async: false
	        method: "GET"
	      
	      edwareDataProxy.getDatafromSource "../data/filter.json", options, (data) ->
	        configs = data
	  )()
	  filter = $('#cpopFilter').edwareFilter $('.filter_label'), configs, edwareComparingPopulations.createPopulationGrid
	  filter.loadReport()