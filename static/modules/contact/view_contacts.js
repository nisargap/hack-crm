angular.module('viewContacts', ['angularify.semantic.dropdown', 'angularify.semantic.modal'])
    .controller('ViewContactController', ['$scope', '$http', function($scope, $http) {
    $scope.show_modal = false;
    $scope.show_text_modal = false;
    $scope.load_send = "";

    $scope.close_modal = function(){
        $scope.show_modal = false;
    }
    $scope.close_text_modal = function(){
        $scope.show_text_modal = false;
    }

    $scope.send_text = function(to_text) {
    	$scope.to_text = to_text;
    	$scope.text_msg = "";
    	$scope.show_text_modal = true;
    }

    $scope.delete_contact = function(email) {

        $http({
          method: 'GET',
          url: '/delete_contact/' + email
        }).then(function successCallback(response) {

            load_contacts();
            console.log(response.data);

        }, function errorCallback(response) {
            // called asynchronously if an error occurs
            // or server returns response with an error status.
            console.log(response.data);
        });

    }

    $scope.send_text_message = function() {
    	$scope.load_send = "active";

    	var data = {
    		"to" : $scope.to_text,
    		"msg" : angular.element( document.querySelector( '#text_msg' ) ).val()
    		}

    	$http.post('/send_text', data).then(function successCallback(response) {


    		$scope.load_send = "";
		    // console.log(response.data);
		    angular.element( document.querySelector( '#text_msg' ) ).val("");

    	}, function errorCallback(response) {
		    // called asynchronously if an error occurs
		    // or server returns response with an error status.

		    $scope.load_send = "";
		    // console.log(response.data);
		    angular.element( document.querySelector( '#text_msg' ) ).val("");


		});

    }
    $scope.send_message = function(){
    	$scope.load_send = "active";
  
    	var data = {
    		"to" : $scope.to_email,
    		"subject" : angular.element( document.querySelector( '#subject' ) ).val(),
    		"msg" : angular.element( document.querySelector( '#msg' ) ).val()
    	}
    	
    	$http.post('/send_email', data).then(function successCallback(response) {
	    // this callback will be called asynchronously
	    // when the response is available

	    $scope.load_send = "";

	    // console.log(response.data);

	    angular.element( document.querySelector( '#subject' ) ).val("");
	   	
	    angular.element( document.querySelector( '#msg' ) ).val("");

	 	}, function errorCallback(response) {
		    // called asynchronously if an error occurs
		    // or server returns response with an error status.

		    $scope.load_send = "";
		    // console.log(response.data);
		});

    }
    $scope.send_email = function(to_email) {
    	$scope.to_email = to_email;
    	$scope.subject = "";
    	$scope.msg = "";
    	$scope.show_modal = true;
    }
    function load_contacts(){
        $http({
    	  method: 'GET',
    	  url: '/get_contacts'
    	}).then(function successCallback(response) {
    	    // this callback will be called asynchronously
    	    // when the response is available

    	    $scope.contacts = response.data;


    	 }, function errorCallback(response) {
    	    // called asynchronously if an error occurs
    	    // or server returns response with an error status.
    	});
    }
    load_contacts();
}]);