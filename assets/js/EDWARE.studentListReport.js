require(['./main'], function (common) {
    require(['cs!EDWARE.studentList', 'cs!edwareUtil'], function (edwareStudentList, edwareUtil) {
		params = edwareUtil.getUrlParams()	
   		edwareStudentList.createStudentGrid(params);
    });
});