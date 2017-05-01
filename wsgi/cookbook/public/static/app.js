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

  app.controller('RecipeController', function ($scope, $http, $timeout) {
    var _this = this;
    this.recipe = recipe;
    this.equipment = recipe.equipment;
    this.ingredients = recipe.ingredients;
    this.instructions = recipe.instructions;

    this.addEquipment = function () {
      this.equipment.push({});
      var elementIndex = this.equipment.length - 1;
      $timeout(function () {
        document.querySelectorAll('.equipment-section .field-input')[elementIndex].focus();
      });
    };

    this.addIngredient = function () {
      this.ingredients.push({});
      var elementIndex = this.ingredients.length - 1;
      $timeout(function () {
        document.querySelectorAll('.ingredients-section .field-input')[elementIndex].focus();
      });
    };

    this.addInstruction = function () {
      this.instructions.push({
        placeholder: 'Step ' + (this.instructions.length + 1),
      });
      var elementIndex = this.instructions.length - 1;
      $timeout(function () {
        document.querySelectorAll('.instructions-section .field-textarea')[elementIndex].focus();
      });
    };

    this.setImage = function (event) {
      var imageFile = event.target.files[0];

      if (!imageFile) {
        return console.log('Image upload: No file selected');
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
        ready: function () {
          _this.debouncedPostImage();
        },
        cropend: function () {
          _this.debouncedPostImage();
        },
        zoom: function () {
          _this.debouncedPostImage();
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

    this.delete = function () {
      var url = window.location.href;
      var data = Object.assign({}, this.recipe);

      $http.delete(url, data)
      .then(function () {
        window.location.href = './';
      }, function () {
        // TODO: display a readable error
        // Server unable to delete
      });
    };

    this.post = function () {
      var url = window.location.href;
      var data = Object.assign({}, this.recipe);

      // Clean up data before submission
      delete data.image;
      data.equipment = data.equipment.filter(x => x.name);
      data.ingredients = data.ingredients.filter(x => x.name);
      data.instructions = data.instructions.filter(x => x.description);

      $http.post(url, data)
      .then(function () {
        document.querySelector('.flash-message').classList.remove('hidden');
        $timeout(function () {
          document.querySelector('.flash-message').classList.add('hidden');
        }, 2000);
      }, function () {
        // TODO: display a readable error
        // Server response error
        // or put way too many characters into a field
      });
    };

    this.postImage = function () {
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
          // These configs allow angular to send files
          headers: {
            'Content-Type': undefined,
          },
          transformRequest: angular.identity,
        })
        .then(function () {
          document.querySelector('.flash-message').classList.remove('hidden');
          $timeout(function () {
            document.querySelector('.flash-message').classList.add('hidden');
          }, 2000);
        }, function () {
          // Server error
        });
      });
    };

    $scope.$watch('rc.recipe', debounce(this.post, 2000), true);
    this.debouncedPostImage = debounce(this.postImage, 2000);

  });
})();

// Returns a function, that, as long as it continues to be invoked, will not
// be triggered. The function will be called after it stops being called for
// N milliseconds. If `immediate` is passed, trigger the function on the
// leading edge, instead of the trailing.
function debounce (func, wait, immediate) {
  var timeout;
  return function () {
    var context = this, args = arguments;
    var later = function () {
      timeout = null;
      if (!immediate) func.apply(context, args);
    };
    var callNow = immediate && !timeout;
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
    if (callNow) func.apply(context, args);
  };
};
