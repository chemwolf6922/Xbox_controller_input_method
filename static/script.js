setInterval(function getData(){
    $.get('/getInfo',function(data){drawKeyboard(data)})
},16);


var keyboardWidth = 1080;
var keybaordHeight = 520;
var keyboardWidthStep = 10.5;
var keyboardHeightStep = 3.0;
var keyList = [
    {key:'Q',centerXStep:0.5,centerYStep:0.5,hand:"left"},
    {key:'W',centerXStep:1.5,centerYStep:0.5,hand:"left"},
    {key:'E',centerXStep:2.5,centerYStep:0.5,hand:"left"},
    {key:'R',centerXStep:3.5,centerYStep:0.5,hand:"left"},
    {key:'T',centerXStep:4.5,centerYStep:0.5,hand:"left"},
    {key:'Y',centerXStep:5.5,centerYStep:0.5,hand:"right"},
    {key:'U',centerXStep:6.5,centerYStep:0.5,hand:"right"},
    {key:'I',centerXStep:7.5,centerYStep:0.5,hand:"right"},
    {key:'O',centerXStep:8.5,centerYStep:0.5,hand:"right"},
    {key:'P',centerXStep:9.5,centerYStep:0.5,hand:"right"},
    {key:'A',centerXStep:1,centerYStep:1.5,hand:"left"},
    {key:'S',centerXStep:2,centerYStep:1.5,hand:"left"},
    {key:'D',centerXStep:3,centerYStep:1.5,hand:"left"},
    {key:'F',centerXStep:4,centerYStep:1.5,hand:"left"},
    {key:'G',centerXStep:5,centerYStep:1.5,hand:"left"},
    {key:'H',centerXStep:6,centerYStep:1.5,hand:"right"},
    {key:'J',centerXStep:7,centerYStep:1.5,hand:"right"},
    {key:'K',centerXStep:8,centerYStep:1.5,hand:"right"},
    {key:'L',centerXStep:9,centerYStep:1.5,hand:"right"},
    {key:'Z',centerXStep:1.5,centerYStep:2.5,hand:"left"},
    {key:'X',centerXStep:2.5,centerYStep:2.5,hand:"left"},
    {key:'C',centerXStep:3.5,centerYStep:2.5,hand:"left"},
    {key:'V',centerXStep:4.5,centerYStep:2.5,hand:"left"},
    {key:'B',centerXStep:6.5,centerYStep:2.5,hand:"right"},
    {key:'N',centerXStep:7.5,centerYStep:2.5,hand:"right"},
    {key:'M',centerXStep:8.5,centerYStep:2.5,hand:"right"}
];
var keyWidth = 90;
var keyHeight = 140;
var LSPosition = {centerXStep:2.5,centerYStep:1.5};
var RSPosition = {centerXStep:7.5,centerYStep:1.5};
var JoystickRadius = 200;

function drawKeyboard(data) {
    var LSX = data.LSX, LSY = -data.LSY, RSX = data.RSX, RSY = -data.RSY;
    if(Math.abs(LSX)<4000 && Math.abs(LSY)<4000){
        LSX = 0;
        LSY = 0;
    }
    if(Math.abs(RSX)<4000 && Math.abs(RSY)<4000){
        RSX = 0;
        RSY = 0;
    }
    var targetKey = data.targetKey;
    var inputText = data.inputText;
    var inputTextBox = document.getElementById("inputText");
    inputTextBox.innerHTML = ":"+inputText;
    var candidates = data.candidates.split(" ");
    var selectedCandidate = data.selectedCandidate;
    if(candidates.length != 0){
        var candidatesText = document.getElementById("candidates");
        candidatesText.innerHTML = ":";
        for(var i=0;i!=candidates.length;i++){
            if(i==selectedCandidate){
                var tempStr = "";
                tempStr += "<font color=\"red\">"
                tempStr += candidates[i];
                tempStr += "</font>"
                tempStr += " ";
                candidatesText.innerHTML += tempStr;
            }else{
                var tempStr = ""
                tempStr += candidates[i];
                tempStr += " ";
                candidatesText.innerHTML += tempStr;
            }   
        }
    }
    
    var canvas = document.getElementById("keyboardCanvas");
    var ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.save();
    ctx.beginPath();
    for(var i=0;i!=keyList.length;i++){
        var key = keyList[i];
        if(key.hand=="left"){
            var centerX = key.centerXStep/keyboardWidthStep * keyboardWidth;
            var centerY = key.centerYStep/keyboardHeightStep * keybaordHeight;
            ctx.rect(centerX-keyWidth/2,centerY-keyHeight/2,keyWidth,keyHeight);
        }
    }
    ctx.stroke();
    ctx.clip();
    ctx.beginPath();
    ctx.fillStyle="rgba(255,0,0,0.2)";
    var centerX = LSPosition.centerXStep/keyboardWidthStep*keyboardWidth + LSX/32767*JoystickRadius;
    var centerY = LSPosition.centerYStep/keyboardHeightStep*keybaordHeight + LSY/32767*JoystickRadius;
    ctx.arc(centerX,centerY,50,0,2*Math.PI);
    ctx.fill();
    ctx.restore();

    ctx.save();
    ctx.beginPath();
    for(var i=0;i!=keyList.length;i++){
        var key = keyList[i];
        if(key.hand=="right"){
            var centerX = (key.centerXStep+0.5)/keyboardWidthStep * keyboardWidth;
            var centerY = key.centerYStep/keyboardHeightStep * keybaordHeight;
            ctx.rect(centerX-keyWidth/2,centerY-keyHeight/2,keyWidth,keyHeight);
        }
    }
    ctx.stroke();
    ctx.clip();
    ctx.beginPath();
    ctx.fillStyle="rgba(255,0,0,0.2)";
    var centerX = (RSPosition.centerXStep+0.5)/keyboardWidthStep*keyboardWidth + RSX/32767*JoystickRadius;
    var centerY = RSPosition.centerYStep/keyboardHeightStep*keybaordHeight + RSY/32767*JoystickRadius;
    ctx.arc(centerX,centerY,50,0,2*Math.PI);
    ctx.fill();
    ctx.restore();

    ctx.save();
    ctx.beginPath();
    for(var i=0;i!=keyList.length;i++){
        var key = keyList[i];
        if(key.key==targetKey){
            var centerX = 0;
            if(key.hand=="left"){
                centerX = key.centerXStep/keyboardWidthStep * keyboardWidth;
            }else{
                centerX = (key.centerXStep+0.5)/keyboardWidthStep * keyboardWidth;
            }
            var centerY = key.centerYStep/keyboardHeightStep * keybaordHeight;
            ctx.fillStyle = "rgba(0,255,0,0.2)";
            ctx.fillRect(centerX-keyWidth/2,centerY-keyHeight/2,keyWidth,keyHeight);
            break;
        }
    }
    ctx.restore();

    ctx.save();
    ctx.beginPath();
    ctx.font = "40px Arial";
    ctx.textAlign = "center";
    for(var i=0;i!=keyList.length;i++){
        var key = keyList[i];
        var centerX = 0;
        if(key.hand=="left"){
            centerX = key.centerXStep/keyboardWidthStep * keyboardWidth;
        }else{
            centerX = (key.centerXStep+0.5)/keyboardWidthStep * keyboardWidth;
        }
        var centerY = key.centerYStep/keyboardHeightStep * keybaordHeight+15;
        ctx.fillText(key.key,centerX,centerY);
    }
    ctx.restore();
    
}