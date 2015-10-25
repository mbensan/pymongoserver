var express = require('express');
var app = express();
var RTree = require('../lib');

var difference = function(a,b){
	return Math.abs(a-b);
}

var rtree = new RTree();

app.post('/close_users', function(req, res){
	var email = req.param('email'),
	    latitude = req.param('latitude'),
	    longitude = req.param('longitude'),
	    distance = req.param('distance');

	var lastLocation = rtree.get(email);
	if(difference(latitude, lastLocation.latitude) < 1 &&
			difference(longitude, lastLocation.longitude)){
		/* En caso de que ubicación haya cambiado, se reemplaza
			en el RTree*/
		rtree.remove(email);
		rtree.insert(email,{ 'x': latitude,
												 'y': longitude,
												 'w': distance,
												 'h': distance
		});
	}
	var closeUsers = rtree.search({'x': latitude,
											 'y': longitude,
											 'w': distance,
											 'h': distance
	});
  res.send(json.stringify(closeUsers));
});