function load_initial_map() {
    var map_img = new Image();
    map_img.src = "images/Iowa_map.jpg";
    var canvas = document.getElementById('map');
    var ctx=canvas.getContext("2d");
    ctx.drawImage(map_img, 0, 0);
}

function test() {
    alert('fuck');
}

function clear_text() {
    var text_input = document.getElementById('text_input');
    text_input.value = "";
}

function clearAll() {
    clear_text();
    load_initial_map();
}

function visualize() {
    var text_input = document.getElementById('text_input');
    if (text_input.length < 2) {
        alert('Invalid redistricting string format!');
        clear_text();
        return;
    }
    var dict = text_input.value;
    dict = dict.substring(1, dict.length - 1);
    var pairs = dict.split(', ');
    if (pairs.length != 99) {
        alert('Invalid redistricting string format!');
        clear_text();
        return;
    }

    load_initial_map();
    var canvas = document.getElementById('map');
    var ctx=canvas.getContext("2d");
    for (var i = 0; i < pairs.length; i++) {
        var pair = pairs[i];
        var tokens = pair.split(": ");
        var precinct = tokens[0];
        var district = tokens[1];
        precinct = precinct.substring(1, precinct.length - 1);
        district = district.substring(1, district.length - 1);
        draw_mark(canvas, ctx, precinct, district);
    }
}

function draw_mark(canvas, ctx, precinct, district) {
    var coordinate = get_location(precinct);
    ctx.beginPath();
    ctx.arc(coordinate[0], coordinate[1], 10, 0, 2 * Math.PI, true);
    ctx.fillStyle = get_color(district);
    ctx.fill();
}

function get_color(district) {
    if (district == '1') {
        return 'red';
    } else if (district == '2') {
        return 'green';
    } else if (district == '3') {
        return 'blue';
    } else if (district == '4') {
        return 'black';
    }
 }

 function get_location(precinct) {
    if (precinct == '1') {
        return [59, 78];
    }
    if (precinct == '2') {
        return [128, 76];
    }
    if (precinct == '3') {
        return [176, 74];
    }
    if (precinct == '4') {
        return [226, 70];
    }
    if (precinct == '5') {
        return [279, 92];
    }
    if (precinct == '6') {
        return [327, 65];
    }
    if (precinct == '7') {
        return [380, 59];
    }
    if (precinct == '8') {
        return [433, 59];
    }
    
     
     return [1000, 1000];
 }

window.onload = load_initial_map;