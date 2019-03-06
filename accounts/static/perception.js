var count=0;
var counter=0;
function disablebutton(){
    if(count===1||count===3){
         document.getElementById("p").disabled=true;
    }
    
    count=count+1;
    console.log(count);
}

function enableit(){
    counter=counter+1;
    if(counter===3){

         document.getElementById("p").disabled=false;

    }            
}
