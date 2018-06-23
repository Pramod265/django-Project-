/**
 * This function creates notification toast
 * @param {object} options - color,duration,icon,container-id,fade-duration.
 * @param {string} color : alert-danger,alert-success,alert-primary,alert-warning,alert-info,alert-classic
 * @param {string} icon
 * @param {string} duration : default - 5000
 * @param {string} container-id : id of the container where toast will be appended
 * @param {string} fade-duration : default - fast
 */
function ohSnap(n,t){var o={color:null,icon:null,duration:"5000","container-id":"ohsnap","fade-duration":"fast"};t="object"==typeof t?$.extend(o,t):o;var a=$("#"+t["container-id"]),e="",i="",h="";t.icon&&(e="<span class='"+t.icon+"'></span> "),t.color&&(i="alert-"+t.color),h=$('<div class="alert '+i+'">'+e+n+"</div>").fadeIn(t["fade-duration"]),a.append(h),h.on("click",function(){ohSnapX($(this))}),setTimeout(function(){ohSnapX(h)},t.duration)}function ohSnapX(n,t){defaultOptions={duration:"fast"},t="object"==typeof t?$.extend(defaultOptions,t):defaultOptions,"undefined"!=typeof n?n.fadeOut(t.duration,function(){$(this).remove()}):$(".alert").fadeOut(t.duration,function(){$(this).remove()})}

/**
 * This function is adding a div in body for ohSnap library to work and ultimately calling ohSnap to make alerts.
 * Thus the user does not require to make a div in every page they want to use alerts
 * @param {string} message 
 * @param {object} options - color,duration,icon,container-id,fade-duration.
 */
function myToast(message,options={}) {
    var elementExists = document.getElementById("ohsnap");
    if (elementExists) {
        ohSnap(message,options);
    }else{
        $('body').append('<div id="ohsnap"></div>');
        ohSnap(message,options);
    }
}


/**
 * Funtion to check if the email is valid or not
 * @param1 {string} email 
 * @return {boolean} true/false.
 */
function validateEmail(sEmail) {
    var filter = /^([\w-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([\w-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$/;
    return (filter.test(sEmail)) ? true : false;
}

$(document).ready(function($) {

    "use strict";

    [].slice.call( document.querySelectorAll( 'select.cs-select' ) ).forEach( function(el) {
        new SelectFx(el);
    } );

    $('.selectpicker').selectpicker;


    $('#menuToggle').on('click', function(event) {
        $('body').toggleClass('open');
    });

    $('.search-trigger').on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        $('.search-trigger').parent('.header-left').addClass('open');
    });

    $('.search-close').on('click', function(event) {
        event.preventDefault();
        event.stopPropagation();
        $('.search-trigger').parent('.header-left').removeClass('open');
    });
});