$(function()
{
    // Semantic API stuff
    // $('selector').api(
    // {
    //     url: '/api/...',
    //     beforeSend: function(settings) 
    //     {   
    //         /* good place for a timeout to wait for typing to stop before requesting autosuggestions from server */
    //         // if (still typing)
    //         //    return false;
    //     },
    //     /*onResponse: function(response) 
    //     {
    //         console.log('API response', response);
    //         return response;
    //     },*/
    //     onFailure: function(response) 
    //     {   // request failed, or valid response but response.success = false
    //         console.log('onFailure', response);
    //     },
    //     onError: function(errorMessage) 
    //     {   // invalid response
    //         console.log('onError', errorMessage);
    //     },
    //     /*onAbort: function(errorMessage) 
    //     {   // navigated to a new page, CORS issue, or user canceled request
            
    //     },*/
    //     successTest: function(response) 
    //     {   // test whether a json response is valid
    //         return response.success || false;
    //     },
    //     onSuccess: function(response) 
    //     {   // HERE'S WHERE WE GET TO THE POINT
    //         //doShitWith(response);
    //     }
    // })
    // ;
    
    // Make dismissable messages dismissable
    $('.message .close')
     .on('click', function() 
    {
        $(this).closest('.message')
         .transition('fade')
    });
    
    // Pop up message on user name after successful login
    $('#logged-in-name.login-success')
     .popup(
    {
        on: 'manual',
        position: 'bottom left',
        context: '#logged-in-name',
        content: 'You are now logged in.',
        onCreate: function(module)
        {
            console.log('this', this);
            console.log('module', module);
            $(this).popup('show');
        },
        onVisible: function(module)
        {
            window.setTimeout(function()
            {
                $(this).popup('hide');
            }, 2000);
        },
        onHidden: function(module)
        {
            $(this).popup('destroy');
            $(module).removeClass("login-success");
        }
    });
});
