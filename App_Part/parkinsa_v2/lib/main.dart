import 'dart:convert';
import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong/latlong.dart';

import 'dart:async';
import 'dart:io';
import 'dart:math';
import 'package:flutter/material.dart';
import 'package:http/http.dart';
import 'package:geolocator/geolocator.dart';
//import 'package:flutter_mapbox_navigation/library.dart';

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ParkINSA Demo',
      theme: ThemeData(
        primarySwatch: Colors.red,
      ),
      home: MyHomePage(title: 'ParkINSA Home Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  // This widget is the home page of your application. It is stateful, meaning
  // that it has a State object (defined below) that contains fields that affect
  // how it looks.

  // This class is the configuration for the state. It holds the values (in this
  // case the title) provided by the parent (in this case the App widget) and
  // used by the build method of the State. Fields in a Widget subclass are
  // always marked "final".

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {

  String _platformVersion = 'Unknown';
  String _instruction = "";
  /*MapBoxNavigation _directions;
  MapBoxOptions _options;

  bool _arrived = false;
  bool _isMultipleStop = false;
  double _distanceRemaining, _durationRemaining;
  MapBoxNavigationViewController _controller;*/
  bool _routeBuilt = false;
  bool _isNavigating = false;
  bool _hasBeenPressed = false;

  static FlutterMap maMap = new FlutterMap(
      options: new MapOptions(
          center: new LatLng(43.571013, 1.465583),
          zoom: 16.0),
      layers:[
        new TileLayerOptions(
            urlTemplate:
            "https://api.mapbox.com/styles/v1/nlokebo/ckiegosj231np19p6f50uhtx7/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoibmxva2VibyIsImEiOiJja2llZ2xtbmQweWZsMnByczBpc3B3N3V0In0.jJly99l_kZv0VV9qGj6vfA",
            additionalOptions: {
              'accessToken':
              'pk.eyJ1Ijoibmxva2VibyIsImEiOiJja2llZ2xtbmQweWZsMnByczBpc3B3N3V0In0.jJly99l_kZv0VV9qGj6vfA',
              'id': 'mapbox.mapbox - streets - v7'
            }),
          new MarkerLayerOptions(
            markers: [
              new Marker(
              width: 80.0,
              height: 80.0,
              point: new LatLng(51.5, -0.09),
              builder: (ctx) =>
              new Container(
              child: new FlutterLogo(),
              ),
            ),
          ]),
      ]
  );
  static var parking;
  /*= GridView.count(
    // Create a grid with 2 columns. If you change the scrollDirection to
    // horizontal, this produces 2 rows.
    crossAxisCount: 5,
    // Generate 100 widgets that display their index in the List.
    children: generateItems(100));*/
  static var myBody;



  List serverResponse = new List();
  int maxPlaces = 0;
  String position ="(2.3,1.2)";//mec qui fait la geolocalisation
  var dept =""; //vient du formulaire utilisateur
  var rng = new Random();
  var lat=0.0, long=0.0;

  @override
  Widget build(BuildContext context) {
    List serverResponse ;
    String position ="(2.3,1.2)";//mec qui fait la geolocalisation
    String dept =""; //vient du formulaire utilisateur
    int cpt = 0;
    var rng = new Random();
    var lat=0.0, long=0.0;
    Color ccolor = Colors.transparent;
    return new Scaffold(
      appBar: new AppBar(
          title: new Text('Park\'INSA'),
          centerTitle:true),
      body: myBody,//myContainer(2,maMap,parking),

        drawer: Drawer(
          child:ListView(
              padding: EdgeInsets.zero,
              children: <Widget>[
                DrawerHeader(
                  child: Align(child:Text("Départements",style: TextStyle(fontSize: 20.0))),
                  decoration: BoxDecoration(
                    color: Colors.red,
                  ),
                ),
                ListTile(
                  title: Text('GEI'),
                  tileColor: ccolor,
                  onTap: () {
                    // Update the state of the app.
                    // ...
                    Navigator.pop(context);
                    dept = "GEI";
                    _makeGetRequest(dept) ;
                    setState(() {
                      ccolor = Colors.lightBlueAccent;
                    });
                  setState(() {
                      parking = GridView.count(
                        // Create a grid with 2 columns. If you change the scrollDirection to
                        // horizontal, this produces 2 rows.
                          crossAxisCount: 5,
                          // Generate 100 widgets that display their index in the List.
                          children: generateItems());
                    });

                  },


                ),
                ListTile(
                  title: Text('GP'),
                  onTap: () async {
                    dept="GP";
                    Navigator.pop(context);
                    _makeGetRequest(dept) ;
                    setState(() {
                      ccolor = Colors.lightBlueAccent;
                    });
                    parking = GridView.count(
                      // Create a grid with 2 columns. If you change the scrollDirection to
                      // horizontal, this produces 2 rows.
                        crossAxisCount: 5,
                        // Generate 100 widgets that display their index in the List.
                        children: generateItems());

                  },
                ),
                ListTile(
                  title: Text('GM'),
                  onTap: () {
                    // Update the state of the app.
                    // ...
                    dept="GM";
                    Navigator.pop(context);
                    _makeGetRequest(dept) ;
                    setState(() {
                      ccolor = Colors.lightBlueAccent;
                    });
                    parking = GridView.count(
                      // Create a grid with 2 columns. If you change the scrollDirection to
                      // horizontal, this produces 2 rows.
                        crossAxisCount: 5,
                        // Generate 100 widgets that display their index in the List.
                        children: generateItems());
                  },
                ),
                ListTile(

                  title: Text('GMM'),
                  onTap: () {
                    // Update the state of the app.
                    // ...
                    dept="GMM";
                    Navigator.pop(context);
                    _makeGetRequest(dept) ;
                    setState(() {
                      ccolor = Colors.lightBlueAccent;
                    });
                    parking = GridView.count(
                      // Create a grid with 2 columns. If you change the scrollDirection to
                      // horizontal, this produces 2 rows.
                        crossAxisCount: 5,
                        // Generate 100 widgets that display their index in the List.
                        children: generateItems());

                  },
                ),
              ],
          )
        ),
        bottomNavigationBar: BottomAppBar(
        shape: const CircularNotchedRectangle(),
          child: Container(height: 50.0,),
          ),
        );

  }

  @override
  void initState() {
    super.initState();

    myBody=myContainer(2,maMap,parking);
    //initialize();
  }

   myContainer(var type, var maMap, var mesPlaces){
    switch (type) {
      case 0:
        return maMap;
      case 1:
        return mesPlaces;
      default:
        return Container(
          color: Colors.grey,
          child: Center(child: Text("Bienvenue à l'INSA")),
        );

    }
  }

   generateItems() {
    var children = <Widget>[];
    for (var i = 0; i < 19; i++) {
      children.add(
          new GestureDetector(
              onTap: (){
                print("Container clicked "+(i+1).toString());
                //myBody = maMap;
                setState(() {
                  if(serverResponse.contains((i+1).toString())){
                    myBody = maMap;}});},
              child:
                Container(
                  width: 20.0,
                  color: serverResponse.contains((i+1).toString()) ? Colors.green:Colors.red,
                  child: Icon(Icons.directions_car),
                  padding: const EdgeInsets.all(2.0),
                  margin: const EdgeInsets.all(2.0),
                )
          )
      );
    }
    return children;
  }
  // Platform messages are asynchronous, so we initialize in an async method.
  /*Future<void> initialize() async {
    // If the widget was removed from the tree while the asynchronous platform
    // message was in flight, we want to discard the reply rather than calling
    // setState to update our non-existent appearance.
    if (!mounted) return;

    _directions = MapBoxNavigation(onRouteEvent: _onEmbeddedRouteEvent);
    _options = MapBoxOptions(
      //initialLatitude: 36.1175275,
      //initialLongitude: -115.1839524,
        zoom: 15.0,
        tilt: 0.0,
        bearing: 0.0,
        enableRefresh: false,
        alternatives: true,
        voiceInstructionsEnabled: true,
        bannerInstructionsEnabled: true,
        allowsUTurnAtWayPoints: true,
        mode: MapBoxNavigationMode.drivingWithTraffic,
        units: VoiceUnits.imperial,
        simulateRoute: false,
        animateBuildRoute: true,
        longPressDestinationEnabled: true,
        language: "en");

    String platformVersion;
    // Platform messages may fail, so we use a try/catch PlatformException.
    try {
      platformVersion = await _directions.platformVersion;
    } on PlatformException {
      platformVersion = 'Failed to get platform version.';
    }

    setState(() {
      _platformVersion = platformVersion;
    });
  }
  Future<void> _onEmbeddedRouteEvent(e) async {
    _distanceRemaining = await _directions.distanceRemaining;
    _durationRemaining = await _directions.durationRemaining;

    switch (e.eventType) {
      case MapBoxEvent.progress_change:
        var progressEvent = e.data as RouteProgressEvent;
        _arrived = progressEvent.arrived;
        if (progressEvent.currentStepInstruction != null)
          _instruction = progressEvent.currentStepInstruction;
        break;
      case MapBoxEvent.route_building:
      case MapBoxEvent.route_built:
        setState(() {
          _routeBuilt = true;
        });
        break;
      case MapBoxEvent.route_build_failed:
        setState(() {
          _routeBuilt = false;
        });
        break;
      case MapBoxEvent.navigation_running:
        setState(() {
          _isNavigating = true;
        });
        break;
      case MapBoxEvent.on_arrival:
        _arrived = true;
        if (!_isMultipleStop) {
          await Future.delayed(Duration(seconds: 3));
          await _controller.finishNavigation();
        } else {}
        break;
      case MapBoxEvent.navigation_finished:
      case MapBoxEvent.navigation_cancelled:
        setState(() {
          _routeBuilt = false;
          _isNavigating = false;
        });
        break;
      default:
        break;
    }
    setState(() {});
  }*/
  _makeGetRequest(var dept) async {
    String list = "";
    //Response response = await get(_localhost(dept, lat, long))
    var codec = new Utf8Codec();
    RawDatagramSocket.bind(InternetAddress.anyIPv4, 0)
        .then((RawDatagramSocket udpSocket) {
      udpSocket.forEach((RawSocketEvent event) {
        if(event == RawSocketEvent.read) {
          Datagram dg = udpSocket.receive();
          list = codec.decode((dg.data));
          list = list.substring(1,list.length-1);
          var tab = list.split(",");
          serverResponse = new List();
          for(int i = 0 ; i < tab.length ; i++){
            serverResponse.add(tab[i]);
          }
          setState(() {
            myBody = parking;
          });
          print(serverResponse);

        }
      });
      var test = udpSocket.send(dept.codeUnits, InternetAddress('192.168.43.68'), 5001);
    });
    /*setState(()  {
      var tmp="";
      int i=0;
      //List list = json.decode(response.body)['res'].toList();
      /*print("Nombre de places "+list[0].toString());
      maxPlaces = list[0];
      for(i=1; i<list.length; i++){
        tmp += " "+list[i].toString();
        serverResponse.add(list[i]);
      }*/
      print("Places disponibles "+list);
      //lat = rng.nextDouble()*180;
      //long = rng.nextDouble()*180;
      //print("La position du departement "+ dept +" est : "+serverResponse + "\n Ma position est : ("+lat.toStringAsFixed(2)+","+long.toStringAsFixed(2) +")");
      //position = await _determinePosition() ;
    });*/
  }
  String _localhost(var dept, var lat, var long) {
    if (Platform.isAndroid){
      return 'http://192.168.43.68:5001?GM';
    //http://10.0.2.2:5000?dept='+dept+"&lat="+lat.toStringAsFixed(2)+"&long="+long.toStringAsFixed(2)
    }
    else{
      print(dept);
      return 'http://localhost:3000?dept='+dept+"&pos=toto";// for iOS simulator
    }

  }

  /// Determine the current position of the device.
  ///
  /// When the location services are not enabled or permissions
  /// are denied the `Future` will return an error.
  Future<Position> _determinePosition() async {
    bool serviceEnabled;
    LocationPermission permission;

    serviceEnabled = await Geolocator.isLocationServiceEnabled();
    if (!serviceEnabled) {
      return null;//return Future.error('Location services are disabled.');
    }

    permission = await Geolocator.checkPermission();
    if (permission == LocationPermission.deniedForever) {
      return null;//Future.error('Location permissions are permantly denied, we cannot request permissions.');
    }

    if (permission == LocationPermission.denied) {
      permission = await Geolocator.requestPermission();
      if (permission != LocationPermission.whileInUse &&
      permission != LocationPermission.always) {
        return null;//Future.error('Location permissions are denied (actual value: $permission).');
      }
    }
    return await Geolocator.getCurrentPosition();
  }

}
