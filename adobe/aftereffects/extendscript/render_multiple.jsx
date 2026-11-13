// Render a composition multiple times while replacing text in a selected text box with lines from a text file
// Example: 
//     You want to render a lower thirds for each subject in a series of interviews.
//     1. Create a text file with each subject's name on a separate line.
//     2. Create the composition for the lower thirds, taking note of the name of the text box that will hold the subject's name.
//     3. Run the script
//     4. Select the composition, the text box, and the text file created in step (1).
// 

var project = app.project;
var composition = project.activeItem;
var textbox;
var compositionName;
var textboxName;
var layer;
var textArray;

function slugify(title) {
    return title
        .toLowerCase()
        .split(' ')
        .map(function (word) {
            return word.split('')
                .filter(function (c) { return c.charCodeAt(0) >= 97 && c.charCodeAt(0) <= 123 })
                .join('')
        }
        ).join('_')
}

function findByName(items, name) {
    for (var i = 0; i < items.length; i++) {
        const item = items[i];
        if (item.name === name) {
            return item;
        }
    }
    alert("Composition not found");
}

function getTextFileLines() {
    var textlines = [];
    var file = File.openDialog("Select newline-separated list of text");
    file.open("r");
    while (!file.eof) {
        textlines.push(file.readln());
    }
    file.close();
    return textlines;
}

function main(){
    
    // Get composition
    compositionName = prompt("Name of target composition (leave blank to use active)", "", "Choose Composition");
    
    if (compositionName != "") {
        composition = findByName(project.items, compositionName);
    }
    
    textbox = composition.layers[1];
    
    // Get text layer
    textboxName = prompt("Name of the textbox layer (leave blank to use first layer)", "", "Choose layer")
    
    if (textboxName != "") {
        textbox = composition.layers.byName(textboxName);
    }
    
    // Get text
    textArray = getTextFileLines();
    
    // Render multiple
    for (var i = 0; i < textArray.length; i++) {
        var text = textArray[i];
        textbox.property("Source Text").setValue(text);
        var renderQueueItem = project.renderQueue.items.add(composition);
        renderQueueItem.outputModule(1).file = new File("output_" + i + "_" + slugify(text) + ".mov");
        project.renderQueue.render();
    }
}

main();
