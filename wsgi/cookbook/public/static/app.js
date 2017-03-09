// TODO: add to build process and minify
(function () {
  var app = angular.module('cookbook', []);

  app.config(['$httpProvider', function ($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    },
  ]);

  app.controller('RecipeController', function ($scope, $http) {
    this.recipe = {};
    this.equipment = [
      { placeholder: 'Wok' },
      { placeholder: 'Broom' },
      { placeholder: 'Magnifying Glass' },
    ];
    this.ingredients = [
      { placeholder: '18 oz. gummy worms' },
      { placeholder: '3 pairs socks' },
      { placeholder: '15 blocks smelly cheese' },
    ];
    this.instructions = [
      { placeholder: 'Step 1', order: 0 },
      { placeholder: 'Step 2', order: 1 },
      { placeholder: 'Step 3', order: 2 },
    ];

    this.addEquipment = function () {
      this.equipment.push({ placeholder: 'Wok' });
    };

    this.addIngredient = function () {
      this.ingredients.push({ placeholder: '18 oz. Gummy Worms' });
    };

    this.addInstruction = function () {
      this.instructions.push({
        placeholder: 'Step ' + (this.instructions.length + 1),
        order: this.instructions.length,
      });
    };

    this.submit = function (recipe) {
      this.recipe.ingredients = this.ingredients;
      this.recipe.equipment = this.equipment;
      this.recipe.instructions = this.instructions;

      // TODO: Watch for changes and post periodically
      $http.post('/recipes/add/', this.recipe)
        .success(function (data, status, headers, config) {
          window.location = '/recipes';
        })
        .error(function (data, status, header, config) {
          // nothing
        });
    };

  });

})();
