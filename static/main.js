/**
  * pushlight-srv
  * main javascript lib
  */

// var table = new Tabulator("#example-table", {
//  	height:"80%", // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
//  	data:tabledata, //assign data to table
//  	layout:"fitColumns", //fit columns to width of table (optional)
//  	columns:[ //Define Table Columns
// 	 	{title:"data_id", field:"data_id", width:"6em"},
// 	 	{title:"pushlight_client_id", field:"pushlight_client_id", width:"2em"},
// 	 	{title:"sensor", field:"sensor", width:3},
//     {title:"lat", field:"lat"},
//     {title:"lon", field:"lon"},
//     {title:"age", field:"age", width:5},
// 	 	{title:"date", field:"date", sorter:"date", hozAlign:"left", width:"8em"},
//     {title:"time", field:"time", sorter:"time", hozAlign:"left", width:"8em"},
//     {title:"altitude", field:"altitude"},
//     {title:"course", field:"course"},
//     {title:"speed_kmph", field:"speed_kmph"},
//     {title:"servo_angle", field:"servo_angle", width:4}
//  	]
// });

// var table = new Tabulator("#example-table", {
//  	height:"80%", // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
//  	data:tabledata, //assign data to table
//   autoColumns: true,
//   autoColumnsDefinitions:[
//       {field:"pushlight_client_id", width:"2em", tooltipsHeader: true},
//       {field:"sensor", width:"2em"},
//       {field:"age", width:"4em"},
//       {field:"date", headerFilter:"datetime", formatter:"datetime", 
//         formatterParams:{
//           inputFormat:"yyyyMMdd",
//           outputFormat:"yyyy-MM-dd",},
//         editorParams:{format:"yyyyMMdd"},
//       },
//       {field:"time",
//         // headerFilter:"time",
//         formatter:"datetime", formatterParams:{
//           inputFormat:"HHmmssuu",
//           outputFormat:"HH:mm:ss",},
//         // editorParams:{format:"HHmmssuu"},
//       },
//       {field:"servo_angle", width:"4em", headerFilter:true},
//   ],
// });


var map = L.map('map')
var markers = [];
var gpsdata = [];
var last_id = 0;

var item_count = 50;



var table = new Tabulator("#example-table", {
  data: gpsdata,
  autoColumns: true,
  autoColumnsDefinitions:[
      {field:"pushlight_client_id", width:"2em", tooltipsHeader: true},
      {field:"sensor", width:"2em"},
      {field:"age", width:"4em"},
      {field:"date", headerFilter:"datetime", formatter:"datetime", 
        formatterParams:{
          inputFormat:"yyyyMMdd",
          outputFormat:"yyyy-MM-dd",},
        editorParams:{format:"yyyyMMdd"},
      },
      // {field:"time",
      //   // headerFilter:"time",
      //   formatter:"datetime", formatterParams:{
      //     inputFormat:"HHmmss",
      //     outputFormat:"HH:mm:ss",},
      //   // editorParams:{format:"HHmmssuu"},
      // },
      {field:"servo_angle", width:"4em", headerFilter:true},
  ],
  layout:"fitColumns",
  resizableColumnFit:true,
});

// trigger an alert message when the row is clicked
table.on("rowClick", function(e, row){
  map.setView([row.getData().lat, row.getData().lon], 18);
});

table.on("dataLoaded", function(data){

  if (data.length == 0) {
    return;
  }

  redraw_gpsview(data);

});

function refresh_data() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      var gpsdata_new = JSON.parse(this.responseText);
      if (gpsdata_new.length > 0) {
        for (gpsdata_row of gpsdata_new) {
          // add new data point to beginning
          gpsdata.unshift(gpsdata_row);
          while (gpsdata.length > item_count) {
            // remove overflowing data points from end of array
            gpsdata.pop();
          }
        }
        table.setData(gpsdata, {});
      }
    }
  };
  xhttp.open("GET", "/items/last?item_count="+item_count+"&last_id="+last_id, true);
  xhttp.send();

  // table.setData("/items/last", { item_count: item_count, last_id: last_id }, "GET"); 
}

function redraw_gpsview(data) {
  map.setView([data[0].lat, data[0].lon], 18);

  L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
  }).addTo(map);

  for (const row of data) {
    // for each new line, remove first element of 'markers' and add to deletion array
    while (markers.length > item_count) {
      map.removeLayer(markers.shift());
    };
    var marker = L.marker([row.lat, row.lon]).addTo(map);
    // add new marker to end of array
    markers.push(marker);
    if (row.data_id > last_id) {
      last_id = row.data_id;
    };
  };
}

setInterval(() => {
  refresh_data();
}, 20000)

setTimeout(() => {
  refresh_data();
}, 500)

function set_item_count() {
  item_count = document.getElementById('item_count').value;
  last_id = 0;
  refresh_data();
}