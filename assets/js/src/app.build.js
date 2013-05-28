({
	appDir: ".",
	baseUrl: "modules",
	dir : "build",
	preserveLicenseComments: false,
	optimize: 'none',
	modules: [
	{
		name : "EDWARE.comparingPopulations"
	},
	
	{
		name : "EDWARE.comparingPopulationsReport"
	},
	{
		name : "EDWARE.individualStudent"
	},
	{
		name : "EDWARE.individualStudentReport"
	},
	{
		name : "EDWARE.studentList",
		exclude : ['jquery']
	},
	{
		name : "EDWARE.studentListReport"
	}]
})