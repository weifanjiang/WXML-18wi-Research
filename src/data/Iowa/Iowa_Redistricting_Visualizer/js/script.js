function load_initial_map() {
    var map_img = new Image();
    map_img.src = "images/Iowa_map.jpg";
    var canvas = document.getElementById('map');
    var ctx=canvas.getContext("2d");
    ctx.drawImage(map_img, 0, 0);
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
        draw_mark(canvas, ctx, precinct, district);
    }
}

function draw_mark(canvas, ctx, precinct, district) {
    var coordinate = get_location(precinct);
    ctx.beginPath();
    ctx.arc(coordinate[0], coordinate[1], 15, 0, 2 * Math.PI, true);
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
     precinct = precinct.toString();
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
     if (precinct == '41') {
        return [599, 175];   
     }
     if (precinct == '42') {
        return [650, 170];   
     }
     if (precinct == '43') {
        return [100, 279];   
     }
     if (precinct == '44') {
        return [163, 277];   
     }
     if (precinct == '45') {
        return [222, 274];   
     }
     if (precinct == '46') {
        return [271, 269];   
     }
     if (precinct == '47') {
        return [324, 266];   
     }
     if (precinct == '48') {
        return [376, 262];   
     }
     if (precinct == '49') {
        return [426, 258];   
     }
     if (precinct == '50') {
        return [477, 248];   
     }
     if (precinct == '51') {
        return [529, 244];   
     }
     if (precinct == '52') {
        return [581, 239];   
     }
     if (precinct == '53') {
        return [631, 225];   
     }
     if (precinct == '54') {
        return [690, 209];   
     }
     if (precinct == '55') {
        return [116, 331];   
     }
     if (precinct == '56') {
        return [172, 330];   
     }
     if (precinct == '57') {
        return [217, 328];   
     }
     if (precinct == '58') {
        return [264, 325];   
     }
     if (precinct == '59') {
        return [313, 322];   
     }
     if (precinct == '60') {
        return [366, 318];   
     }
     if (precinct == '61') {
        return [423, 312];   
     }
     if (precinct == '62') {
        return [482, 306];   
     }
     if (precinct == '63') {
        return [534, 301];   
     }
     if (precinct == '64') {
        return [586, 297];   
     }
     if (precinct == '65') {
        return [636, 277];   
     }
     if (precinct == '66') {
        return [699, 252];   
     }
     if (precinct == '67') {
        return [151, 386];   
     }
     if (precinct == '68') {
        return [218, 382];   
     }
     if (precinct == '69') {
        return [268, 378];   
     }
     if (precinct == '70') {
        return [320, 373];   
     }
     if (precinct == '71') {
        return [371, 371];   
     }
     if (precinct == '72') {
        return [424, 367];   
     }
     if (precinct == '73') {
        return [473, 359];   
     }
     if (precinct == '74') {
        return [525, 356];   
     }
     if (precinct == '75') {
        return [576, 352];   
     }
     if (precinct == '76') {
        return [627, 361];   
     }
     if (precinct == '77') {
        return [640, 320];   
     }
     if (precinct == '78') {
        return [696, 291];   
     }
     if (precinct == '79') {
        return [142, 429];   
     }
     if (precinct == '80') {
        return [195, 426];   
     }
     if (precinct == '81') {
        return [245, 425];   
     }
     if (precinct == '82') {
        return [298, 422];   
     }
     if (precinct == '83') {
        return [348, 416];   
     }
     if (precinct == '84') {
        return [400, 411];   
     }
     if (precinct == '85') {
        return [452, 409];   
     }
     if (precinct == '86') {
        return [503, 405];   
     }
     if (precinct == '87') {
        return [555, 398];   
     }
     if (precinct == '88') {
        return [602, 403];   
     }
     if (precinct == '89') {
        return [640, 407];   
     }
     if (precinct == '90') {
        return [146, 471];   
     }
     if (precinct == '91') {
        return [197, 469];   
     }
     if (precinct == '92') {
        return [250, 469];   
     }
     if (precinct == '93') {
        return [301, 464];   
     }
     if (precinct == '94') {
        return [351, 460];   
     }
     if (precinct == '95') {
        return [403, 456];   
     }
     if (precinct == '96') {
        return [455, 450];   
     }
     if (precinct == '97') {
        return [508, 445];   
     }
     if (precinct == '98') {
        return [557, 440];   
     }
     if (precinct == '99') {
        return [610, 448];   
     }
     
     return [1000, 1000];
 }

window.onload = load_initial_map;
