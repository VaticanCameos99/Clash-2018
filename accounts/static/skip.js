
            var count=0;
            var x;
                
        function Getme(){
            count=count+1;

            x=count;
            if(count%3===0){
            document.getElementById("img").src=images[x];
            }

            console.log(count);
        }
        function Reduceme(){
            count=count-3;

            x=count;
            if(count===3||count===6||count===9||count===12||count===15||count===18||count===0){
            document.getElementById("img").src=images[x];
            }

                        console.log(count);

        }
        var images=[]
        images[0]="0.png";
        images[3]="1.jpg";
        images[6]="2.jpg";
        images[9]="3.jpg";
        images[12]="4.jpg";
        images[15]="5.jpg";
        images[18]="6.png";
        images[21]="7.png";
      