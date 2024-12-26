
var steps=10

const socket = io("/ctlstep");


function reload_popovers() {
    $('[data-bs-toggle="popover"]').popover(
        {html: true, animation: true}
    );
}

function raise_error(msg) {
   $.toast({
       heading: 'Error',
       text: msg,
       loader: true,
       loaderBg: '#9EC600',
       position: 'top-center',
   });
}

function init_chat() {
   socket.on('connect', function () {
       console.log("Connected to socketio");
   });
   socket.on('connected', function(msg) {
       console.log("Connected!");
       console.log(msg);
   });

// FB 2024-12-06 ----- manages all send buttons
   $("#sendform").submit(function(event) {
       event.preventDefault();
       //  $('#send_msg').val()
       //vvv  = $(this).val()
       vvv = document.activeElement.value
       console.log(vvv)
       // to_call = $('#to_call').val();
       steps = $('#tune_step').val();
       msg = {'cmd': vvv,'steps': steps};
       socket.emit("send",msg);  
       console.log(msg);       
   });
   $("#deeng").click(function() {
       console.log("Deenergize")
       msg= ''; 
       socket.emit("deeng",msg);  
   });
    
}

