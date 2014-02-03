module.exports = function(grunt){

    require("matchdep").filterDev("grunt-*").forEach(grunt.loadNpmTasks);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            css: {
                files: ['_scss/**/*.scss'],
                tasks: ['css'],
                options: {
                  livereload: true,
                }
            },
            js: {
                files: ['_js/**/*.js'],
                tasks: ['uglify'],
                options: {
                  livereload: true,
                }
            },
            jekyll: {
                files: ['**/*.html', 'main.min.*', 'fonts/**/*', 'images/**/*', '**/*.md'],
                tasks: ['jekyll:build'],
                options: {
                  livereload: true,
                }
            }
        },
        jekyll: {
            build: {
                src: '.',
                dest: '_site'
            }
        },
        uglify: {
            build: {
                files: {
                    'main.min.js': ['_js/jquery-1.10.2.min.js', '_js/jquery.slides.min.js', '_js/main.js', '_js/**/*.js']
                }
            }
        },
        sass: {
            build: {
                files: {
                    'main.min.css': '_scss/main.scss'
                }
            }
        },
        cssmin: {
            build: {
                src: 'main.min.css',
                dest: 'main.min.css'
            }
        },
        cssc: {
            build: {
                options: {
                    consolidateViaDeclarations: true,
                    consolidateViaSelectors:    true,
                    consolidateMediaQueries:    true
                },
                files: {
                    'main.min.css': 'main.min.css'
                }
            }
        }
    });

    grunt.registerTask('default', []);
    grunt.registerTask('css', ['sass', 'cssc', 'cssmin']);
};