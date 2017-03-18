// TODO: add to build process and minify
(function () {
  var app = angular.module('cookbook', []);

  app.config(['$httpProvider', function ($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    },
  ]);

  app.controller('RecipeController', function ($scope, $http) {
    this.recipe = {
      title: 'New Recipe',
      description: 'Write a description for the brilliant new recipe you came up with that makes your mouth water',
      serves: 'Serves 5',
      time: '30 - 40 min',
    };
    this.equipment = [
      { name: 'Rolling pin' },
      { name: 'Cake tin' },
    ];
    this.ingredients = [
      { name: '3 cups of flour' },
      { name: '1 stick of butter' },
    ];
    this.instructions = [
      { description: 'This is what you do first...', placeholder: 'Step 1', order: 0 },
      { placeholder: 'Step 2', order: 1 },
      { placeholder: 'Step 3', order: 2 },
    ];

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
      $http.post('/recipes/create', this.recipe)
        .success(function (data, status, headers, config) {
          window.location = '/recipes';
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
