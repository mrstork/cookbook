// TODO: add to build process and minify
(function () {
  var app = angular.module('cookbook', []);
  var cropper;

  app.config(['$httpProvider', function ($httpProvider) {
      // Allows form submission with django csrf protection
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
      // Allows form to send files
      $httpProvider.defaults.headers.post['Content-Type'] = undefined;
      $httpProvider.defaults.transformRequest = angular.identity;
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

      if (cropper) {
        var _this = this;
        var data = this.recipe;
        cropper.getCroppedCanvas().toBlob(function (blob) {
          blob.name = Date.now() + '.png';
          data.image = blob;
          _this.post();
        }, 'image/png');

      } else {
        this.post();
      }
    };

    this.publish = function () {
      this.recipe.draft = false;
      this.submit();
    };

    // TODO: Watch for changes and post periodically
    this.post = function () {
      var url = window.location.href;
      var formdata = toFormData(this.recipe);
      $http.post(url, formdata)
        .then(function () {
          window.location = '/recipes'
        }, function () {
          // TODO: display a readable error
        });
    }

  });
})();

function toFormData (object) {
  var form = new FormData();
  var toString = Object.prototype.toString;

  for (var key in object) {
    if (object.hasOwnProperty(key)) {
      var value = object[key];
      var type = toString.call(value).slice(8, -1);
      switch (type) {
        case 'Array':
        case 'FileList':
          form.append(key, value.map(function (entry) {
            return toFormData(entry);
          }));
          break;
        case 'Object':
          form.append(key, toFormData(value));
          break;
        case 'Blob':
          form.append(key, value, value.name);
          break;
        case 'File':
        default:
          form.append(key, value);
      }
    }
  }

  return form;
}
