
$(document).ready(function(){
    
    
    $('#contactusform').on('submit', function(evt){
        ///when an end user submits a form this is what is called
        
        
        ///if this was not in place the form would lead to a differnt page
        evt.preventDefault();
        
        
      
        var name = $('#name').val();
        var email = $('#email').val();
        var contactnum = $('#contactnum').val();
        var message = $('#message').val();
        
        
        var params = { name: name, email: email, contactnum: contactnum
                             ,message: message};
        
        $.ajax({"url": '/contactus', "method": "post", "data":params, "dataType": 'json'})
            .done(function(response){
                
                
                
                
                alert(response['message']);
                
            });
        
        
        
        
    });
    
    
    
});