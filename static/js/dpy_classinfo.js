

/**
   * This function posts an ajax-request to add class session's.
   * @param none
   */
  function add_class_session(_parent,class_data) {

    var session = [];
    var sd = $('#session_start_id option:selected').val();
    var ed = $('#session_end_id option:selected').val();

    session.push({'ic':parseInt(ic_id),'start_month':parseInt(sd),'end_month':parseInt(ed)});
    $.ajax({
        url: profiling_urls.addsession, 
        method: "POST",
        data:{
          'data':JSON.stringify(session),
          csrfmiddlewaretoken: g_csrftoken
        }
    }).done(function(resp) {
        if(resp.status == true){
            myToast("<h5>"+resp.message+"</h5>",{color:'success'});
        }
    }).fail(function(err) {
      var msg = "Oops something went wrong!!!";
      if (err.responseJSON) {
        console.log(err.responseJSON);
        // (err.responseJSON.non_field_errors) ? msg = err.responseJSON.non_field_errors.join():false;
      }
      myToast(msg,{color:'danger'});
    });    
  }//End

$(document).ready(function () {
  /**
   * This function adds class session by calling ajax request.
   * @param none
   */
  $(".submit-session").click(function() {
    
    add_class_session();


  });
  // end

});
// End of ready function