require(['./main'], function (common) {
    require(['cs!EDWARE.individualStudent', 'cs!edwareUtil'], function (edwareIndividualStudent, edwareUtil) {
		params = edwareUtil.getUrlParams();
	    
    	edwareIndividualStudent.generateIndividualStudentReport(params);
    });
});