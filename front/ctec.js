var fileInput = document.getElementById("csvFileInput");
var csvFile = fileInput.files[0];

var reader = new FileReader();
reader.readAsText(csvFile);
reader.onload = function(event) {
    var csvData = event.target.result;
    var data = [];
    var rows = csvData.split("\n");
    for (var i = 0; i < rows.length; i++) {
        data.push(rows[i].split(","));
    }

    try {
        var headers = data[0];
    } catch (e) {
        console.error("Error in accessing columns: ", e);
        return;
    }

    var owners = new Set();

    for (var i = 1; i < data.length; i++) {
        var row = data[i];

        var name = row[headers.indexOf("Name")];
        var company = row[headers.indexOf("Owner")];
        var ownerName = row[headers.indexOf("Primary Owner First Name")] + " " + row[headers.indexOf("Primary Owner Last Name")];
        var siteAddress = row[headers.indexOf("Site Address")];
        var ownerAddress = row[headers.indexOf("Street Address")];
        var city = row[headers.indexOf("City")];
        var state = row[headers.indexOf("State")];
        var zipcode = row[headers.indexOf("Zip")];
        var county = row[headers.indexOf("County")];
    }
}