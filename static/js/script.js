$(function()
{
    $('selector').api(
    {
        url:
        onResponse: function(response) 
        {
            console.log('API response', response);
            return response;
        },
        successTest: function(response) 
        {
            // test whether a json response is valid
            return response.success || false;
        },
        onSuccess: function(response) 
        {
            // valid response and response.success = true
        },
        onFailure: function(response) 
        {
            // request failed, or valid response but response.success = false
        },
        onError: function(errorMessage) 
        {
            // invalid response
        },
        onAbort: function(errorMessage) 
        {
            // navigated to a new page, CORS issue, or user canceled request
        }
    })
    ;

});
