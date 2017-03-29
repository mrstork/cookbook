'use strict';

const gulp = require('gulp');
const path = require('path');

const sass = require('gulp-sass');
const cssmin = require('gulp-clean-css');
const autoprefixer = require('gulp-autoprefixer');

const imagemin = require('gulp-imagemin');
const pngquant = require('imagemin-pngquant');

var config = {
  // images_directory: ['./wsgi/cookbook/public/static/images/', './wsgi/media/'],
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
  return gulp.src(['**/*.png', '**/*.jpg', '**/*.gif', '**/*.svg'])
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
    .pipe(gulp.dest('.'));
});


gulp.task('default', function () {
  gulp.watch(path.join(config.scss_directory, '**/*.scss'), ['scss']);
});
