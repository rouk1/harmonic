module.exports = function (grunt) {
	require('load-grunt-tasks')(grunt);

	var BUNDLES = {
		'src/assets/js/landing.bundle.js': ['src/assets/js/landing.js']
	};

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),

		browserify: {
			dev: {
				options: {
					watch: true,
					browserifyOptions: {
						debug: true
					},
					transform: [
						['babelify', {presets: ['es2015']}],
						['stringify', {}]
					]
				},
				files: BUNDLES
			},
			dist: {
				options: {
					browserifyOptions: {
						debug: false
					},
					transform: [
						['babelify', {presets: ['es2015']}],
						['stringify', {}],
						['uglifyify', {
							global: true
						}]
					]
				},
				files: BUNDLES
			}
		},

		watch: {
			assets: {
				files: [
					'src/assets/fonts/**/*.{eot,svg,ttf,woff}',
					'src/assets/sounds/**/*.{mp3,ogg,wav}',
					'src/assets/img/**/*.{jpg,png,svg,ico,icns}',
					'src/assets/video/**/*.{mp4,ogv,webm}',
					'src/assets/js/*.bundle.js',
					'src/assets/css/**/*.css',
					'src/templates/**/*.html'
				],
				options: {
					livereload: true,
					interrupt: true
				}
			}
		},

		clean: {
			release: ['src/assets/css', 'src/assets/js/*.bundle.js']
		}
	});

	grunt.registerTask('default', ['browserify:dev', 'watch']);
	grunt.registerTask('build', ['browserify:dist']);
};
