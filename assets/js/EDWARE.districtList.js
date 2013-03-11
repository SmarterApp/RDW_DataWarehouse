require(['./main'], function (common) {
    require(['cs!edwareDistrictList', 'cs!edwareUtil'], function (edwareDistrictList, edwareUtil) {
		params = edwareUtil.getUrlParams()	
   		edwareDistrictList.createComparePopulationGrid(params);
    });
});