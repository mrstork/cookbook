'use strict';

var cssmin = require('gulp-clean-css');
var gulp = require('gulp');
var imagemin = require('gulp-imagemin');
var path = require('path');
var pngquant = require('imagemin-pngquant');
var sass = require('gulp-sass');

var config = {
  images_directory: './wsgi/cookbook/public/static/images/',
  scss_directory: './wsgi/cookbook/public/scss/',
  static_directory: './wsgi/cookbook/public/static/',
};

gulp.task('scss', function () {
  gulp.src(path.join(config.scss_directory, 'main.scss'))
    .pipe(sass.sync().on('error', sass.logError))
    .pipe(cssmin({keepSpecialComments: 0}))
    .pipe(gulp.dest(config.static_directory));
});

gulp.task('images', function () {
  return gulp.src(config.images_directory)
    .pipe(imagemin({
      optimizationLevel: 7,
      multipass: true,
      progressive: true,
      svgoPlugins: [
        {
          removeViewBox: false,
        },
      ],
      use: [pngquant()],
    }))
    .pipe(gulp.dest(config.static_directory));
});


gulp.task('default', function () {
  gulp.watch(path.join(config.scss_directory, '**/*.scss'), ['scss']);
});
