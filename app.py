<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CitizenVoice</title>
<style>
body { font-family: Arial; background:#eef2f3; margin:0; padding:0; display:flex; justify-content:center; }
#chat { width: 100%; max-width: 500px; height: 90vh; overflow-y: auto; padding:10px; background:white; border-radius:10px; margin-top:10px; }
.bubble { padding:12px; margin:5px 0; max-width:80%; border-radius:15px; }
.bot { background:#f1f1f1; }
.user { background:#1faa59; color:white; margin-left:auto; }
button.option { background:#1faa59; color:white; border:none; border-radius:30px; padding:10px 20px; margin:3px; cursor:pointer; }
</style>
</head>
<body>
<div id="chat"></div>

<script>
const chat = document.getElementById('chat');

function addBot(message, speak=true){
    const div = document.createElement('div');
    div.className = 'bubble bot';
    div.innerText = message;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
    if(speak){
        const utter = new SpeechSynthesisUtterance(message);
        utter.lang = 'es-ES';
        speechSynthesis.speak(utter);
    }
}

function addUser(message){
    const div = document.createElement('div');
    div.className = 'bubble user';
    div.innerText = message;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

function askArea(){
    addBot('¿Sobre qué área quieres opinar?');
    ['Urbanismo','Limpieza','Movilidad','Seguridad','Parques','Otra'].forEach(a=>{
        const btn = document.createElement('button');
        btn.className='option';
        btn.innerText=a;
        btn.onclick=()=>{
            addUser(a);
            area=a;
            chat.innerHTML=''; // siguiente pregunta limpia chat
            askTipo();
        }
        chat.appendChild(btn);
    });
}

function askTipo(){
    addBot('¿Es una incidencia o propuesta?');
    ['Incidencia','Propuesta'].forEach(t=>{
        const btn = document.createElement('button');
        btn.className='option';
        btn.innerText=t;
        btn.onclick=()=>{
            addUser(t);
            tipo=t;
            askDescripcion();
        }
        chat.appendChild(btn);
    });
}

function askDescripcion(){
    addBot('Describe tu mensaje usando voz o texto.');
    const input = document.createElement('input');
    input.type='text';
    input.placeholder='Escribe aquí o pulsa 🎤';
    input.style.width='70%';
    const mic = document.createElement('button');
    mic.innerText='🎤';
    mic.onclick=()=>{
        if(window.hasOwnProperty('webkitSpeechRecognition')){
            var recognition = new webkitSpeechRecognition();
            recognition.lang='es-ES';
            recognition.onresult=function(e){
                input.value=e.results[0][0].transcript;
            }
            recognition.start();
        }
    }
    const submit = document.createElement('button');
    submit.innerText='Enviar';
    submit.onclick=()=>{
        addUser(input.value);
        descripcion=input.value;
        askPuntuacion();
    }
    chat.appendChild(input);
    chat.appendChild(mic);
    chat.appendChild(submit);
}

function askPuntuacion(){
    addBot('Valora el servicio (1 = Muy malo, 5 = Excelente)');
    for(let i=1;i<=5;i++){
        const btn = document.createElement('button');
        btn.className='option';
        btn.innerText=i;
        btn.onclick=()=>{
            addUser(i);
            puntuacion=i;
            askUbicacion();
        }
        chat.appendChild(btn);
    }
}

function askUbicacion(){
    addBot('Detectando ubicación 📍...');
    navigator.geolocation.getCurrentPosition((pos)=>{
        lat=pos.coords.latitude;
        lon=pos.coords.longitude;
        addBot('¡Listo! Gracias por participar.');
        // Aquí enviar datos a Google Sheets via API / Google Forms
        console.log({area,tipo,descripcion,puntuacion,lat,lon});
    });
}

let area='', tipo='', descripcion='', puntuacion=0, lat=0, lon=0;

askArea();

</script>
</body>
</html>
