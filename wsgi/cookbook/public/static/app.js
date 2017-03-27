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
        order: this.instructions.length,
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
      var formdata = Object.toFormData(this.recipe);
      $http.post(url, formdata)
        .then(function () {
          window.location = '/recipes'
        }, function () {
          // TODO: display a readable error
        });
    }

  });
})();

// TODO: Remove all this extra crap below, and build your own abridged version

/*
 object-to-formdata v0.1.2
 https://github.com/nervgh/object-to-formdata
*/
(function(window) {
    'use strict';

    var Blob = window.Blob;
    var File = window.File;
    var FileList = window.FileList;
    var FormData = window.FormData;

    var isSupported = (Blob && File && FileList && FormData);
    var toString = Object.prototype.toString;
    var forEach = Array.prototype.forEach;
    var map = Array.prototype.map;

    if (!isSupported) return;

    /**
     * Returns type of anything
     * @param {Object} any
     * @returns {String}
     */
    function getType(any) {
        return toString.call(any).slice(8, -1);
    }
    /**
     * Converts path to FormData name
     * @param {Array} path
     * @returns {String}
     */
    function toName(path) {
        var array = map.call(path, function(value) {
            return '[' + value + ']';
        });
        array[0] = path[0];
        return array.join('');
    }

    /**
     * Converts object to FormData
     * @param {Object} object
     * @returns {FormData}
     */
    function toFormData(object) {
        var form = new FormData();
        var cb = function(node, value, key, path) {
            var type = getType(value);

            switch (type) {
                case 'Array':
                    break; // step into
                case 'Object':
                    break; // step into
                case 'FileList':
                    forEach.call(value, function(item, index) {
                        var way = path.concat(index);
                        var name = toName(way);
                        form.append(name, item);
                    });
                    return true; // prevent step into
                case 'File':
                    var name = toName(path);
                    form.append(name, value);
                    return true; // prevent step into
                case 'Blob':
                    var name = toName(path);
                    form.append(name, value, value.name);
                    return true; // prevent step into
                default:
                    var name = toName(path);
                    form.append(name, value);
                    return true; // prevent step into
            }
        };

        Object.traverse(object, cb, null, null, true);

        return form;
    }

    // export
    Object.toFormData = toFormData;

}(window));


/*
 object-traverse v0.1.1
 https://github.com/nervgh/object-traverse
*/
(function(window) {
    'use strict';

    var MAX_DEPTH = 100;
    var getKeys = Object.keys;
    var isNaN = window.isNaN;
    /**
     * Returns "true" if any is object
     * @param {*} any
     * @returns {Boolean}
     */
    function isObject(any) {
        return any instanceof Object;
    }
    /**
     * Returns "true" if any is number
     * @param {*} any
     * @returns {Boolean}
     */
    function isNumber(any) {
        return typeof any === 'number' && !isNaN(any);
    }
    /**
     * Walks object recursively
     * @param {Object} object
     * @param {Function} cb
     * @param {*} ctx
     * @param {Boolean} mode
     * @param {Boolean} ignore
     * @param {Number} max
     * @returns {Object}
     */
    function walk(object, cb, ctx, mode, ignore, max) {
        var stack = [[], 0, getKeys(object).sort(), object];
        var cache = [];

        do {
            var node = stack.pop();
            var keys = stack.pop();
            var depth = stack.pop();
            var path = stack.pop();

            cache.push(node);

            while(keys[0]) {
                var key = keys.shift();
                var value = node[key];
                var way = path.concat(key);
                var strategy = cb.call(ctx, node, value, key, way, depth);

                if (strategy === true) {
                    continue;
                } else if (strategy === false) {
                    stack.length = 0;
                    break;
                } else {
                    if(max <= depth || !isObject(value)) continue;

                    if (cache.indexOf(value) !== -1) {
                        if (ignore) continue;
                        throw new Error('Circular reference');
                    }

                    if (mode) {
                        stack.unshift(way, depth + 1, getKeys(value).sort(), value);
                    } else {
                        stack.push(path, depth, keys, node);
                        stack.push(way, depth + 1, getKeys(value).sort(), value);
                        break;
                    }
                }
            }
        } while(stack[0]);

        return object;
    }
    /**
     * Walks object recursively
     * @param {Object} object
     * @param {Function} callback
     * @param {*} [context]
     * @param {Number} [mode=0]
     * @param {Boolean} [ignoreCircularReferences=false]
     * @param {Number} [maxDepth=100]
     * @returns {Object}
     */
    function traverse(object, callback, context, mode, ignoreCircularReferences, maxDepth) {
        var cb = callback;
        var ctx = context;
        var _mode = mode === 1;
        var ignore = !!ignoreCircularReferences;
        var max = isNumber(maxDepth) ? maxDepth : MAX_DEPTH;

        return walk(object, cb, ctx, _mode, ignore, max);
    }

    // export
    Object.traverse = traverse;

}(window));
