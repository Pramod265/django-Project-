    var g_auth = localStorage.getItem("auth");
    if(g_auth == null) {
        g_auth = sessionStorage.getItem("auth");
    }

    if(g_auth) {
        try {
            g_auth = JSON.parse(g_auth);
        } catch(error) {
            g_auth = null; 
        }
    }

    var getCookie = function(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    };
    var g_csrftoken = getCookie('csrftoken');

    var initLogin = function() {
        if(g_auth) {
            $('.btn-logout').show();
            console.log("Logged User: ",g_auth.username);
            if(g_auth.remember_me) {
                localStorage.setItem("auth", JSON.stringify(g_auth));
            } else {
                sessionStorage.setItem("auth", JSON.stringify(g_auth));
            }
        } else {
            // $('#non-logged-in').show();
            // $('.btn-logout').hide();
        }
    };

    $(function () {
        initLogin();

        // $('#testAuthButton').click(function() {
        //     $.ajax({
        //         url: g_urls.test_auth, 
        //         method: "GET", 
        //         beforeSend: function(request) {
        //             if(g_auth) {
        //                 request.setRequestHeader("Authorization", "Token " + g_auth.key);
        //             }
        //         }
        //     }).done(function(data) {
        //         $('#test-auth-response').html("<span class='label label-success'>Ok! Response: " + data);
        //     }).fail(function(data) {
        //         $('#test-auth-response').html("<span class='label label-error'>Fail! Response: " + data.responseText + " (status: " + data.status+")</span>");
        //     });
        // });
        
        $('.login-btn').click(function() {
            var username = $("#username").val();
            var password = $('#password').val();
            var remember_me = $('#remember-me').prop('checked');
            if(username && password) {
                console.log("Will try to login with ", username, password);
                $.ajax({
                    url: g_urls.login, 
                    method: "POST", 
                    data: {
                        username: username,
                        password: password,
                        csrfmiddlewaretoken: g_csrftoken
                    }
                }).done(function(data) {
                    console.log("DONE: ", username, data.key);
                    g_auth = {
                        username: username,
                        key: data.key,
                        remember_me: remember_me
                    };
                    initLogin();
                    // CAREFUL! csrf token is rotated after login: https://docs.djangoproject.com/en/1.7/releases/1.5.2/#bugfixes
                    g_csrftoken = getCookie('csrftoken');
                    window.location.href = '/dashboard/home'
                }).fail(function(data) {
                    console.log("FAIL", data);
                });
            } else {
                // $('#modal-error').removeClass('d-invisible');
            }
        });

        $('.btn-logout').click(function() {
            console.log("Trying to logout");
            $.ajax({
                url: g_urls.logout, 
                method: "POST", 
                beforeSend: function(request) {
                    request.setRequestHeader("Authorization", "Token " + g_auth.key);
                },
                data: {
                    csrfmiddlewaretoken: g_csrftoken
                }
            }).done(function(data) {
                console.log("DONE: ", data);
                g_auth = null;
                localStorage.removeItem("auth");
                sessionStorage.removeItem("auth");
                initLogin();
                window.location.href = '/'
            }).fail(function(data) {
                console.log("FAIL: ", data);
            });
        });
    });