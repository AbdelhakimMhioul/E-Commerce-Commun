
document.querySelectorAll('#add').forEach(item => {
    item.addEventListener('click',function(){
     
        let productId=this.dataset.product
        let action =this.dataset.action
      //Send Data to the url: /send_data/
      let xmlhttp = new XMLHttpRequest();  // new HttpRequest instance 
      let Url = "/send_data/"; //the url that we want send data to
      xmlhttp.open("POST",Url,true); //Send a POST data
      xmlhttp.setRequestHeader('X-CSRFToken',csrftoken);  // Add a CSRF token 
      xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
      let body=JSON.stringify({'productId':productId,'action':action}) 
      xmlhttp.send(body); //We want to send the productId and the action
      xmlhttp.onerror = function(){
          alert("La requête a échoué");
      };
      
  })
})
document.querySelectorAll('#remove').forEach(item => {
    item.addEventListener('click',function(){
        let productId=this.dataset.product
        let action =this.dataset.action
        Send_Data(productId,action)
        let div=document.getElementById(productId)
        div.remove()
       
    })
  })
  document.querySelectorAll('#plus').forEach(item => {
    item.addEventListener('click',function(){
        let productId=this.dataset.product
        let action =this.dataset.action
        Send_Data(productId,action)
       
    })
  })
  document.querySelectorAll('#moins').forEach(item => {
    item.addEventListener('click',function(){
        let productId=this.dataset.product
        let action =this.dataset.action
        Send_Data(productId,action)
       
    })
  })
    function Send_Data(productId,action)
    {
        //Send Data to the url: /send_data/
        let xmlhttp = new XMLHttpRequest();  // new HttpRequest instance 
        let Url = "/send_data/"; //the url that we want send data to
        xmlhttp.open("POST",Url,true); //Send a POST data
        xmlhttp.setRequestHeader('X-CSRFToken',csrftoken);  // Add a CSRF token 
        xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        let body=JSON.stringify({'productId':productId,'action':action}) 
        xmlhttp.send(body); //We want to send the productId and the action
        xmlhttp.onerror = function(){
         alert("La requête a échoué");
        };
        location.reload()   
    }

