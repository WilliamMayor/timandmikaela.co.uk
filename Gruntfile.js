module.exports = function(grunt){

    require("matchdep").filterDev("grunt-*").forEach(grunt.loadNpmTasks);

    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        watch: {
            html: {
                files: ['_site/**/*.html'],
                tasks: ['htmlhint'],
                options: {
                  livereload: true,
                }
            },
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
                files: ['**/*.html', 'main.min.*', 'fonts/**/*', 'images/**/*'],
                tasks: ['jekyll:build'],
                options: {
                  livereload: true,
                }
            }
        },
        htmlhint: {
            build: {
                options: {
                    'tag-pair': true,
                    'tagname-lowercase': true,
                    'attr-lowercase': true,
                    'attr-value-double-quotes': true,
                    'doctype-first': true,
                    'spec-char-escape': true,
                    'id-unique': true,
                    'head-script-disabled': true,
                    'style-disabled': true
                },
                src: ['_site/**/*.html']
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