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

var table = new Tabulator("#example-table", {
 	height:"80%", // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
 	data:tabledata, //assign data to table
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
      {field:"time",
        // headerFilter:"time",
        formatter:"datetime", formatterParams:{
          inputFormat:"HHmmssuu",
          outputFormat:"HH:mm",},
        // editorParams:{format:"HHmmssuu"},
      },
      {field:"servo_angle", width:"4em", headerFilter:true},
  ],
});
// trigger an alert message when the row is clicked
table.on("rowClick", function(e, row){
  alert("Row " + row.getData().data_id + " Clicked!!!!");
});