// TODO: add to build process and minify
(function () {
  var app = angular.module('cookbook', []);

  app.config(['$httpProvider', function ($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    },
  ]);

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

    this.submit = function () {
      this.recipe.ingredients = this.ingredients;
      this.recipe.equipment = this.equipment;
      this.recipe.instructions = this.instructions;

      // TODO: Watch for changes and post periodically
      $http.post(window.location.href, this.recipe)
        .success(function (data, status, headers, config) {
          // nothing
        })
        .error(function (data, status, header, config) {
          // nothing
        });

    };

    this.publish = function () {
      this.recipe.draft = false;
      this.submit();
    };

  });

})();
