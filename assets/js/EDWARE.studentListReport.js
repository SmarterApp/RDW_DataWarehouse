require(['./main'], function (common) {
    require(['cs!EDWARE.studentList', 'cs!edwareUtil'], function (edwareStudentList, edwareUtil) {
		params = edwareUtil.getUrlParams()	
	    params.districtId = parseInt(params.districtId)
	    params.schoolId = parseInt(params.schoolId)
	    
    		edwareStudentList.createStudentGrid(params);
    });
});