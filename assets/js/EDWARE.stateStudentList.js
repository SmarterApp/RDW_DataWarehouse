require(['./main'], function (common) {
    require(['cs!edwareStateStudentList', 'cs!edwareUtil'], function (edwareStateStudentList, edwareUtil) {
		params = edwareUtil.getUrlParams()	
   		edwareStateStudentList.createComparePopulationGrid(params);
    });
});