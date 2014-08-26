var src_dir = process.argv[2],
    license_path = process.argv[3];

(function(src_dir, license){
    // required modules
    var fs = require('fs'),
        path = require('path'),
        walk = require('walk'),
        pf = require('prepend-file');

    // variable declaration
    var content, walker;

    // read in license text
    content = fs.readFileSync(path.resolve(license), {
        encoding: "utf-8"
    });

    walker = walk.walk(src_dir);

    // walk down source directory and append license information
    walker.on('file', function(root, fileStats, next) {
        var filename = fileStats.name;
        if (/\.js$/.test(filename)) {
            var file_path = path.resolve(root, filename);
            pf(file_path, content, function(done) {
                if (done) {
                    console.log('added license information to ' + filename);
                }
            });
        }
        next();
    });

    // recursively
    walker.on('directories', function(root, dirStatsArray, next) {
        next();
    });
})(src_dir, license_path);
