  /**
   * This function posts an ajax-request to add class session's.
   * @param none
   */
  function add_class_session() {

    var session = [];
    var sd = $('#session_start_id option:selected').val();
    var ed = $('#session_end_id option:selected').val();

    session.push({'ic':parseInt(ic_id),'start_month':parseInt(sd),'end_month':parseInt(ed)});
    $.ajax({
        url: profiling_urls.addsession, 
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        csrfmiddlewaretoken: g_csrftoken,
        data : JSON.stringify(session),
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

  /**
   * This function posts an ajax-request to get class attendance.
   * @param {string} date
   */
  function get_class_attendance(date) {
    $('.att-tbody').empty();
    $('.att-reset-toggle').addClass('d-none');
    $.ajax({
        url: '/profiling/day-attendance/?ic='+parseInt(ic_id)+'&type=1&date='+date, 
        method: "get",
        csrfmiddlewaretoken: g_csrftoken,
        data : {},
    }).done(function(resp) {
        if(!isEmpty(resp.data)){
            var srno = 0,td='',is_day=false;
            $.each(resp.data, function(index,value){
              var status = '<button data-user_id='+value.user+' class="btn btn-danger btn-sm mark-attendance">A</button>';
              if (value.attendance) {
                if (value.attendance[date]) {
                  is_day = true;
                  var status = '<button data-user_id='+value.user+' data-id='+value.attendance[date]['id']+' class="btn btn-success btn-sm mark-attendance">P</button>';
                }else{
                  var status = '<button data-user_id='+value.user+' data-id='+value.attendance[date]['id']+' class="btn btn-danger btn-sm mark-attendance">A</button>';
                }
              }
              td+='<tr>'
                    +'<td class="text-center">'+(++srno)+'</td>'
                    +'<td class="text-center">'+(value.roll_no?value.roll_no:'-')+'</td>'
                    +'<td>'+value.first_name+(value.middle_name?' '+value.middle_name:'')+' '+value.last_name+'</td>'
                    +'<td class="text-center">'+status+'</td>'
                 +'</tr>';
            });
            $('.att-tbody').html(td);
            (is_day===true)?$('.att-reset-toggle').removeClass('d-none'):$('.att-reset-toggle').addClass('d-none');
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

  /**
   * This function posts an ajax-request to mark school's class attendance.
   * @param {none}
   */
  function mark_school_student_attendance() {
    var date = $('#att-date').val();
    var absent = [],present = [];
    $('.mark-attendance').each(function(){
      if ($(this).text().trim().toLowerCase()=='p' && !$(this).attr('data-id')) {
        present.push({'date':date,'user':$(this).attr('data-user_id'),'marked_by':logged_user_id,'institute':logged_institute});
      }
      if ($(this).text().trim().toLowerCase()=='a' && $(this).attr('data-id')) {
        // absent.push({'id':$(this).attr('data-id'),'date':date,'user':$(this).attr('data-user_id'),'marked_by':logged_user_id,'institute':logged_institute});
        absent.push($(this).attr('data-id'));
      }      
    });
    // console.log(absent,present);return false;
    $.ajax({
        url: '/profiling/day-attendance/',
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        csrfmiddlewaretoken: g_csrftoken,
        data : JSON.stringify({'absent':absent,'present':present}),
    }).done(function(resp) {
      myToast("<h6>"+resp.message+"</h6>",{color:'success'});
      get_class_attendance(date);
    }).fail(function(err) {
      var msg = "Oops something went wrong!!!";
      if (err.responseJSON) {
        console.log(err.responseJSON);
        // (err.responseJSON.non_field_errors) ? msg = err.responseJSON.non_field_errors.join():false;
      }
      myToast(msg,{color:'danger'});
    }); 
  }//End

  /**
   * This function get class session with subjects.
   * @param none
   */
  function getClassSession() {
    $('#sess-sub-pill,#sess-sub-pill-data').empty();
    $.ajax({
        url: '/profiling/session/?ic='+ic_id,
        method: "GET",
        data:{}
    }).done(function(resp) {
      var d1='',d2='',session = 0;
      var month_arr = {1 : 'January', 2 : 'February', 3 : 'March', 4 : 'April', 5 : 'May', 6 : 'June', 7 : 'July', 8 : 'August', 9 : 'September', 10 : 'October', 11 : 'November', 12 : 'December'};
      $.each(resp.data,function(index,value){
        d2+='<div class="list-group list-group-flush">'
          +'<a class="list-group-item bg-secondary text-white py-2"><b>Start Month: '+month_arr[value.start_month]+'</b><b class="ml-4">End Month: '+month_arr[value.end_month]+'</b></a>';
                
        d1+= '<a class="nav-link active" data-toggle="pill" href="#v-pills-'+value.id+'">Session '+(++session)+'</a>';
        $.each(value.subject,function(key,val){
          d2+='<a href="javascript:" class="list-group-item list-group-item-action list-group-item-light py-1">'+val.name+'</b>';
        });
        d2+='</div>';
      });
      $('#sess-sub-pill').html(d1);
      $('#sess-sub-pill-data').html(d2);
    }).fail(function(err) {
      var msg = "Oops something went wrong!!!";
      myToast(msg,{color:'danger',duration:2000});
    });
  }//End

  /**
   * This function get class subjects.
   * @param none
   */
  function getClassSubjects() {
    $('.append-class-subjects').empty();
    $.ajax({
        url: '/profiling/session-sub/?ic='+ic_id,
        method: "GET",
        data:{}
    }).done(function(resp) {
      var d = '';
      $.each(resp.data,function(index,value){
        d+= '<div class="ml-2 custom-control custom-radio">'
              +'<input value="'+value.name+'" data-subject_id="'+value.id+'" type="radio" id="cr-sub-'+value.id+'" name="crds1" class="custom-control-input">'
              +'<label class="custom-control-label" for="cr-sub-'+value.id+'">'+value.name+'</label>'
            +'</div>';
      });
      $('.append-class-subjects').html(d);
    }).fail(function(err) {
      var msg = "Oops something went wrong!!!";
      myToast(msg,{color:'danger',duration:2000});
    });
  }//End


$(document).ready(function () {
  /**
   * This function gets class session data by calling ajax request.
   * @param none
   */
  $('#nav-subject-tab').one('click',function(){
    getClassSession();
  });//End

  /**
   * This function adds class session by calling ajax request.
   * @param none
   */
  $(".submit-session").click(function() {
    add_class_session();
  });// end

  /**
   * This function gets and append attendance data on first tab click.
   * @param none
   */
  $('#nav-attendance-tab').one('click',function(){
    (log_inst_nature == 1) ? get_class_attendance($('#att-date').val()):false;
  });//End

  /**
   * This function gets and append attendance data on date change.
   * @param none
   */
  $('#att-date').change(function(){
    (log_inst_nature == 1) ? get_class_attendance($('#att-date').val()):false;
  });//End

  /**
   * This function changes attendance toggle state on-click absent-toggle button.
   * @param none
   */
  $('.att-a-toggle').click(function(){
    $('.mark-attendance').removeClass('btn-danger').removeClass('btn-success');
    $('.mark-attendance').addClass('btn-danger').html('A');
  });//End

  /**
   * This function changes attendance toggle state on-click present-toggle button.
   * @param none
   */
  $('.att-p-toggle').click(function(){
    $('.mark-attendance').removeClass('btn-danger').removeClass('btn-success');
    $('.mark-attendance').addClass('btn-success').html('P');
  });

  /**
   * This function changes attendance toggle state on-click reset-toggle button.
   * @param none
   */
  $('.att-reset-toggle').click(function(){
    (log_inst_nature == 1) ? get_class_attendance($('#att-date').val()):false;
  });

  /**
   * This function marks attendance on student-wise.
   * @param none
   */
  $('body').delegate('.mark-attendance','click',function(){
    ($(this).text().trim().toLowerCase()=='a')?$(this).removeClass('btn-danger').addClass('btn-success').html('P'):$(this).removeClass('btn-success').addClass('btn-danger').html('A');
  });

  /**
   * This function marks attendance for whole student.
   * @param none
   */
  $('.submit-attendance').click(function(){
    (log_inst_nature == 1) ? mark_school_student_attendance():false;
  });


});
// End of ready function