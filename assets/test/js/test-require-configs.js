/*globals require */
var baseConfigs = {
	paths : {	
	    cs: '../../js/3p/cs',
	    'coffee-script': '../../js/3p/coffee-script',
	    jquery: '../../js/3p/jquery-1.7.2.min',
	    jqGrid: '../../js/3p/jquery.jqGrid.min',
	    sourceJS: '../../js',
	    text: '../../js/3p/text',
		mustache: '../../js/3p/mustache',
		templates: '../../js/templates',
		
	    EDWARE: '../../js/EDWARE',
	    edwareUtil: '../../js/EDWARE.util',
	    edwareDataProxy: '../../js/EDWARE.dataProxy',
	    edwareGrid: '../../js/widgets/grid/EDWARE.grid.tablegrid',
	    edwareGridFormatters: '../../js/widgets/grid/EDWARE.grid.formatters',
	    edwareStudentList: '../../js/EDWARE.studentList',
	    edwareIndividualStudent: '../../js/EDWARE.individualStudent',
	    edwareBreadcrumbs: '../../js/widgets/breadcrumb/EDWARE.breadcrumbs',
	    
	    edwareBreadcrumbsTemplate: '../../js/widgets/breadcrumb/template.html'
	},
	shim: {
        'jqGrid': {
            //These script dependencies should be loaded before loading
            //jqGrid
            deps: ['jquery'],
            
            exports: 'jqGrid'
        }
   }
};

require.config(baseConfigs);

function getTestFile() {
	var scriptTags = document.getElementsByTagName("script"), i, testfile = [], fileName;

	for( i = 0; i < scriptTags.length; i++) {
		fileName = scriptTags[i].getAttribute("data-testfile");
		if(fileName) {
			testfile.push(fileName);
		}
	}

	return testfile;
}

require(getTestFile());