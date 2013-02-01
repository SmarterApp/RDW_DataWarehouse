require({
  paths: {
    cs: '3p/cs',
    'coffee-script': '3p/coffee-script',
    jquery: '3p/jquery-1.7.2.min',
    jqGrid: '3p/jquery.jqGrid.min',
    edwareUtil: 'EDWARE.util'
  }
});

require([
  'cs!app'
], function (app) {
	app.initialize();
});
