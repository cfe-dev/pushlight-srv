/**
  * pushlight-srv
  * main javascript lib
  */

const map = L.map('map');
const tileLayer = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
}).addTo(map);

const markers = [];
const gpsdata = [];

let last_id = 0;
let item_count = 50;

const table = new Tabulator("#main-table", {
  data: gpsdata,
  autoColumns: true,
  autoColumnsDefinitions: [
    { field: "data_id", widthGrow: 0.8 },
    { field: "pushlight_client_id", widthGrow: 0.3 },
    { field: "age", widthGrow: 0.5 },
    { field: "servo_angle", widthGrow: 0.5 },
    {
      field: "datetime", widthGrow: 2,
      headerFilter: "input",
      sorter: "datetime", sorterParams: { format: "YYYY-MM-DDTHH:mm:ss.SSSZ", alignEmptyValues: "top", },
          // formatter: "datetime", formatterParams: {
          // inputFormat: "YYYY-MM-DDTHH:mm:ss.SSSZ",
          // outputFormat: "MM/DD/YY hh:mm:ss A", invalidPlaceholder: true
        // },
    },
      // {field:"date", visible:false },
      // {field:"time", visible:false },
      // {field:"date", headerFilter:"datetime", formatter:"datetime",
      //   formatterParams:{
      //     inputFormat:"yyyyMMdd",
      //     outputFormat:"yyyy-MM-dd",},
      //   editorParams:{format:"yyyyMMdd"},
      // },
      // {field:"time",
      //   // headerFilter:"time",
      //   formatter:"datetime", formatterParams:{
      //     inputFormat:"HHmmss",
      //     outputFormat:"HH:mm:ss",},
      //   // editorParams:{format:"HHmmssuu"},
      // },      
  ],
  layout: "fitColumns",
  // layoutColumnsOnNewData:true,
  resizableColumnFit: true,
  movableColumns: true,
});

table.on("rowClick", function(e, row){
  map.setView([row.getData().lat, row.getData().lon], 18);
});

// table.on("dataLoaded", function(data){
//   if (data.length == 0) {
//     return;
//   }
// //   redraw_gpsview(data);
// });

const xhttp = new XMLHttpRequest();
xhttp.timeout = 2000;

xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    let gpsdata_new = JSON.parse(this.responseText);
    if (gpsdata_new.length > 0) {
      for (gpsdata_row of gpsdata_new) {
        // add new data point to beginning
        gpsdata.unshift(gpsdata_row);
        while (gpsdata.length > item_count) {
          // remove overflowing data points from end of array
          let gpsdata_obsolete = gpsdata.pop();
          delete gpsdata_obsolete;
        }
        if (gpsdata_row.data_id > last_id) {
          last_id = gpsdata_row.data_id;
        };
      }
      table.setData(gpsdata, {});
      table.moveColumn("datetime", "age", true);
      redraw_gpsview(gpsdata);
    }
  }
};

function refresh_data(repeat) {

  if (!(xhttp.readyState == 0 || xhttp.readyState == 4)) {
    // skip on pending operation
  } else {
    xhttp.open("GET", "/items/last?item_count=" + item_count + "&last_id=" + last_id, true);
    xhttp.send();
  }

  // table.setData("/items/last", { item_count: item_count, last_id: last_id }, "GET"); 
  if (repeat) {
    setTimeout(() => {
      refresh_data(true);
    }, 20000)
  }
}

function redraw_gpsview(data) {
  map.setView([data[0].lat, data[0].lon], 18);

  for (const row of data) {
    // for each new line, remove first element of 'markers' remove/delete
    while (markers.length > item_count) {
      // map.removeLayer(markers.shift());
      let marker_del = markers.shift();
      marker_del.remove();
      delete marker_del;
    };
    let marker = L.marker([row.lat, row.lon]).addTo(map);
    // add new marker to end of array
    markers.push(marker);
  };
}

function set_item_count() {
  item_count = document.getElementById('item_count').value;
  last_id = 0;
  refresh_data(false);
}