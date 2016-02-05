'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');

gulp.task('scss', function () {
  gulp.src('./wsgi/cookbook/general/styles/cookbook.scss')
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(gulp.dest('./wsgi/cookbook/general/static/'));
});

gulp.task('default', function () {
  gulp.watch('./wsgi/cookbook/general/styles/*.scss', ['scss']);
});
