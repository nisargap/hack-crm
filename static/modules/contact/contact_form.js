angular.module('addContact', ['angularify.semantic.modal'])
    .controller('ContactController', ['$scope', '$http', function($scope, $http) {

    $scope.show_modal = false;
    $scope.close_modal = function(){
        $scope.show_modal = false;
    }

    $scope.add_contact = function(){

      $scope.show_dimmer = true;

      $http.defaults.headers.common['Authorization'] = 'Basic ' + btoa("admin" + ':' + "secret");

      if (!$scope.address) {
        $scope.address = "";
      }
      if (!$scope.profile_img) {
        $scope.profile_img = "";
      }
    	var req = {
		 method: 'POST',
		 url: '/add_contact',
		 data: { name: $scope.name, 
            email: $scope.email, 
            company: $scope.company, 
            address : $scope.address, 
            profile_img: $scope.profile_img,
            phone : $scope.phone }
		}

		$http(req).then(function successCallback(response) {
		    // this callback will be called asynchronously
		    // when the response is available

		    $scope.show_modal = true;

		    console.log(response.data);

		}, function errorCallback(response) {
		    // called asynchronously if an error occurs
		    // or server returns response with an error status.

		    // Debug: console.log(response);
        console.log(response.data);
		});
    }
}]);