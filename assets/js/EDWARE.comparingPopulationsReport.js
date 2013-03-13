require(['./main'], function (common) {
    require(['cs!EDWARE.comparingPopulations', 'cs!edwareUtil'], function (edwareComparingPopulations, edwareUtil) {
		params = edwareUtil.getUrlParams()	
   		edwareComparingPopulations.createPopulationGrid(params);
    });
});