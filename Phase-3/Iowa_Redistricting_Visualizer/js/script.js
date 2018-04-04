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
     if (precinct == '9') {
         return [484, 52];   
     }
     if (precinct == '10') {
         return [535, 56];   
     }
     if (precinct == '11') {
        return [585, 55];   
     }
     if (precinct == '12') {
        return [65, 124];   
     }
     if (precinct == '13') {
        return [127, 122];   
     }
     if (precinct == '14') {
        return [177, 117];   
     }
     if (precinct == '15') {
        return [230, 114];   
     }
     if (precinct == '16') {
        return [335, 108];   
     }
     if (precinct == '17') {
        return [383, 105];   
     }
     if (precinct == '18') {
        return [437, 101];   
     }
     if (precinct == '19') {
        return [489, 98];   
     }
     if (precinct == '20') {
        return [543, 124];   
     }
     if (precinct == '21') {
        return [596, 116];   
     }
     if (precinct == '22') {
        return [68, 175];   
     }
     if (precinct == '23') {
        return [130, 172];   
     }
     if (precinct == '24') {
        return [181, 171];   
     }
     if (precinct == '25') {
        return [233, 168];   
     }
     if (precinct == '26') {
        return [285, 156];   
     }
     if (precinct == '27') {
        return [338, 161];   
     }
     if (precinct == '28') {
        return [388, 156];   
     }
     if (precinct == '29') {
        return [440, 150];   
     }
     if (precinct == '30') {
        return [491, 141];   
     }
     if (precinct == '31') {
        return [90, 228];   
     }
     if (precinct == '32') {
        return [146, 225];   
     }
     if (precinct == '33') {
        return [191, 223];   
     }
     if (precinct == '34') {
        return [242, 219];   
     }
     if (precinct == '35') {
        return [292, 209];   
     }
     if (precinct == '36') {
        return [344, 212];   
     }
     if (precinct == '37') {
        return [398, 209];   
     }
     if (precinct == '38') {
        return [445, 201];   
     }
     if (precinct == '39') {
        return [496, 186];   
     }
     if (precinct == '40') {
        return [547, 180];   
     }
     
     return [1000, 1000];
 }

window.onload = load_initial_map;
