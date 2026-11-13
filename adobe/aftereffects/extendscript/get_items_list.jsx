// Export a list of all items in the current After Effects project as a comma-separated values (CSV) file.
var file = File.saveDialog("Where to save the items list");
file.open("w"); //open in 'write' mode
file.writeln("index,id,name");
var items = app.project.items;
for (var i = 1; i < items.length; i++) {
	file.writeln([i, items[i].id, items[i].name].join(","));
}
file.close();
if (file.created){
	alert("Wrote " + items.length + " items to " + file.path + "/" + file.name)
} else {
	alert("Failed to write items list")
}
