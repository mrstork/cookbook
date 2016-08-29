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
      {
        name_placeholder: 'Gummy Worms',
        quantity_placeholder: 18,
        measurement_placeholder: 'oz.',
      },
      {
        name_placeholder: 'Socks',
        quantity_placeholder: 3,
        measurement_placeholder: 'pairs',
      },
      {
        name_placeholder: 'Smelly Cheese',
        quantity_placeholder: 15,
        measurement_placeholder: 'block',
      },
    ];
    this.instructions = [
      { placeholder: 'Step 1' },
      { placeholder: 'Step 2' },
      { placeholder: 'Step 3' },
    ];

    this.addEquipment = function () {
      this.equipment.push({ placeholder: 'Wok' });
    };

    this.addIngredient = function () {
      this.ingredients.push({
        name_placeholder: 'Gummy Worms',
        quantity_placeholder: 18,
        measurement_placeholder: 'oz.',
      });
    };

    this.addInstruction = function () {
      this.instructions.push({ placeholder: 'Step ' + (this.instructions.length + 1) });
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
