require(['./main'], function (common) {
    require(['cs!EDWARE.schoolList', 'cs!edwareUtil'], function (edwareSchoolList, edwareUtil) {
		params = edwareUtil.getUrlParams()	
   		edwareSchoolList.createStudentGrid(params);
    });
});