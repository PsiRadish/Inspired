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
     
    if (($('#tumblr-import-bttn')).length) // on add chapter page
    {
        console.log('guh');
        
        $.getJSON("/api/tumblr-import.json", function(data) // get tumblr data
        {
            // console.log(data);
            $('#tumblr-import-bttn').removeClass("loading");
            
            // show import pane when button clicked
            $('#tumblr-import-bttn').on('click', function(e)
            {   e.preventDefault();
                console.log('Anything?');
                $('#tumblr-import-pane').toggleClass("collapsed");
                console.log('panel', $('#tumblr-import-pane'));
            });
            
            showBlogs(null);
            function showBlogs(e)
            {
                if (e)
                {
                    e.preventDefault();
                }
                
                $('#import-list').empty();
                
                Object.keys(data).forEach(function(blogName)
                {
                    var link = $('<a href="#"><i class="fa fa-folder-o"></i> ' + blogName + '</a>');
                    
                    var listItem = $('<li>').append(link);
                    $('#import-list').append(listItem);
                    
                    link.data('blogName', blogName);
                    link.on('click', showBlogPosts);
                });
            }
            
            function showBlogPosts(e)
            {
                e.preventDefault();
                
                var blogName = $(this).data('blogName');
                console.log('blogName', blogName);
                
                var posts = data[blogName];
                
                $('#import-list').empty();
                
                // link to go back up to blog list
                var backLink = $('<a href="#"><span class="fa-stack fa">' +
                                 '<i class="fa fa-folder-open-o fa-stack-1x"></i>' +
                                 '<i class="fa fa-long-arrow-up fa-stack-1x"></i>' +
                                 '</span>' + blogName + '</a>');
                
                var listItem = $('<li>').append(backLink);
                $('#import-list').append(listItem);
                
                backLink.on('click', showBlogs);
                
                // make link for each post
                posts.forEach(function(post, index)
                {                    
                    var link = $('<a href="#"><i class="fa fa-file-text-o"></i> ' + post.title + '</a>');
                    post.tags.forEach(function(tag)
                    {
                        link.append('<label class="ui red mini label">' + tag + '</label>');
                    });
                    
                    listItem = $('<li>').append(link);
                    
                    $('#import-list').append(listItem);
                    
                    link.data('blogName', blogName);
                    link.data('postIndex', index);
                    link.on('click', importFromPost);
                });
            }
            
            function importFromPost(e)
            {
                e.preventDefault();
                
                var blogName = $(this).data('blogName');
                var postIndex = $(this).data('postIndex');
                
                var post = data[blogName][postIndex];
                
                $('#title-box').val(post.title);
                $('#body-box').val(post.body);
            }
        });
    }
    
    // Semantic UI pop up message on user name after successful login
    // (Doesn't work yet)
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
