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

        $('#username,#password').on('keypress',function(event) {
            if (event.which == 13 || event.which == 10) {
                    $('.login-btn').trigger('click');
                    event.preventDefault();
            }
            // Prevent default posting of form
        });
        
        $('.login-btn').click(function() {
            var username = $("#username").val();
            var password = $('#password').val();
            var remember_me = $('#remember-me').prop('checked');
            if(username && password) {
                console.log("Will try to login with ", username);
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
                    console.log(data);
                    g_auth = {
                        username: username,
                        key: data.key,
                        remember_me: remember_me
                    };
                    initLogin();
                    // CAREFUL! csrf token is rotated after login: https://docs.djangoproject.com/en/1.7/releases/1.5.2/#bugfixes
                    g_csrftoken = getCookie('csrftoken');
                    // window.location.href = '/dashboard/home'
                    if (data.institute_info.length > 1) {
                        var d = '';
                        $.each(data.institute_info,function(key,value){
                            d+='<div class="card card bg-light mb-3 btn select-institute" data-inst_id="'+value.institute.id+'" style="max-width: 18rem;">'
                                  +'<div class="card-header">'+value.institute.name+'</div>'
                                  +'<div class="card-body">'
                                    +'<p class="card-text">Adress: '+value.institute.address+'</p>'
                                    +'<p class="card-text">City: '+value.institute.city+'</p>'
                                    +'<p class="card-text">Pin-Code: '+value.institute.pin_code+'</p>'
                                  +'</div>'
                                +'</div>';
                        });
                        $('.multi-inst-body').html(d);
                        $('#multi-inst-modal').modal({backdrop:'static',keyboard:false});
                    }else{
                        window.location.href = '/dashboard/home'
                    }
                }).fail(function(err) {
                    var msg = "Oops something went wrong!!!";
                    if (err.responseJSON) {
                        var msg = (err.responseJSON.non_field_errors) ? err.responseJSON.non_field_errors.join():"Oops something went wrong!!!";
                    }
                    myToast(msg,{color:'danger',duration:2000});
                });
            } else {
                // $('#modal-error').removeClass('d-invisible');
                myToast("Please provide credentials!",{color:'danger',duration:2000});
            }
        });

        $('.btn-logout').click(function() {
            console.log("Trying to logout");
            $.ajax({
                url: g_urls.logout, 
                method: "POST", 
                beforeSend: function(request) {
                    if( g_auth ) {
                        if (g_auth.key)
                        request.setRequestHeader("Authorization", "Token " + g_auth.key);
                    }
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

        $('body').delegate('.select-institute','click',function() {
            var institute_id = $(this).attr('data-inst_id');
            $.ajax({
                url: g_urls.set_institute, 
                method: "POST", 
                beforeSend: function(request) {
                    (g_auth.key) ? request.setRequestHeader("Authorization", "Token " + g_auth.key):false;
                },
                data: {
                    institute_id: institute_id,
                    csrfmiddlewaretoken: g_csrftoken
                }
            }).done(function(data) {
                window.location.href = '/dashboard/home'
            }).fail(function(data) {
                console.log("FAIL: ", data);
            });            
        });

    });