/*globals require */
var baseConfigs = {
	paths : {	
	    cs: '../../js/3p/cs',
	    'coffee-script': '../../js/3p/coffee-script',
	    jquery: '../../js/3p/jquery-1.7.2.min',
	    jqGrid: '../../js/3p/jquery.jqGrid.min',
	    sourceJS: '../../js',
	    
	    EDWARE: '../../js/EDWARE',
	    edwareUtil: '../../js/EDWARE.util'
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