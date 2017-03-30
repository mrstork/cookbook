// TODO: add to build process and minify
(function () {
  var app = angular.module('cookbook', []);
  var cropper;

  app.config(['$httpProvider', function ($httpProvider) {
      // Allows form submission with django csrf protection
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    },
  ]);

  // Evaluates contents when a new file is selected
  app.directive('fileChange', function() {
    return {
      restrict: 'A',
      link: function (scope, element, attrs) {
        element.bind('change', scope.$eval(attrs.fileChange));
      }
    };
  });

  app.controller('RecipeController', function ($scope, $http) {
    this.recipe = recipe;
    this.equipment = recipe.equipment;
    this.ingredients = recipe.ingredients;
    this.instructions = recipe.instructions;

    this.addEquipment = function () {
      this.equipment.push({});
      // TODO: focus newly added element
    };

    this.addIngredient = function () {
      this.ingredients.push({});
      // TODO: focus newly added element
    };

    this.addInstruction = function () {
      this.instructions.push({
        placeholder: 'Step ' + (this.instructions.length + 1),
      });
      // TODO: focus newly added element
    };

    $scope.setImage = function () {
      var imageFile = event.target.files[0];

      if (!imageFile) {
        return console.log('No file selected');
      }

      if (imageFile.size > 1e6) {
        return console.log('File too big');
      }

      var imageURL = URL.createObjectURL(imageFile);
      var imageElement = document.querySelector('.image-container img');

      if (cropper) {
        return cropper.replace(imageURL);
      }

      imageElement.src = imageURL;
      cropper = new Cropper(imageElement, {
        aspectRatio: 16 / 9,
        autoCropArea: 0.9,
        minCropBoxWidth: 700,
        center: false,
        cropBoxMovable: false,
        cropBoxResizable: false,
        dragMode: 'move',
        highlight: false,
        restore: false,
        toggleDragModeOnDblclick: false,
        cropend: function (event) {
          // image changed
        },
        zoom: function (event) {
          // image changed
        },
      });
    };

    this.submit = function () {
      this.recipe.ingredients = this.ingredients;
      this.recipe.equipment = this.equipment;
      this.recipe.instructions = this.instructions;
      this.post();
    };

    this.publish = function () {
      this.recipe.draft = false;
      this.submit();
    };

    // TODO: Watch for changes and post periodically
    this.post = function () {
      var _this = this;
      var url = window.location.href;
      var data = Object.assign({}, this.recipe);
      delete data.image;

      $http.post(url, data)
      .then(function () {
        if (cropper) {
          _this.postImage();
        } else {
          window.location = '/recipes'
        }
      }, function () {
        // TODO: display a readable error
        console.log('error');
      });
    };

    this.postImage = function () {
      var _this = this;
      cropper.getCroppedCanvas({
        width: 800,
        height: 450,
      }).toBlob(function (blob) {
        var url = window.location.href;
        var filename = Date.now() + '.png';
        var formdata = new FormData();
        formdata.append('id', _this.recipe.id);
        formdata.append('user', _this.recipe.user);
        formdata.append('image', blob, filename);
        $http.post(url, formdata, {
          // Allows angular to send files
          headers: {
            'Content-Type': undefined,
          },
          transformRequest: angular.identity,
        })
        .then(function () {
          window.location = '/recipes'
        }, function () {
          // TODO: display a readable error
        });
      }, 'image/png');
    };

  });
})();
