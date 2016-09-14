'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var cssmin = require('gulp-clean-css');

gulp.task('scss', function () {
  gulp.src('./wsgi/cookbook/public/scss/main.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(cssmin({keepSpecialComments: 0}))
    .pipe(gulp.dest('./wsgi/cookbook/public/static/'));
});

gulp.task('default', function () {
  gulp.watch('./wsgi/cookbook/public/scss/*.scss', ['scss']);
});
