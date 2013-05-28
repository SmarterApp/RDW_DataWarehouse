({
	appDir: ".",
	baseUrl: "modules",
	dir : "build",
	preserveLicenseComments: false,
	optimize: 'uglify',
	modules: [
	{
		//exclude jquery to avoid duplication
		name : "EDWARE.comparingPopulations",
		exclude : ['jquery']
	},
	
	{
		name : "EDWARE.comparingPopulationsReport"
	},
	{
		name : "EDWARE.individualStudent",
		exclude : ['jquery']
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