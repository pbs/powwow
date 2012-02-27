/*
 * This js file is part of the PowWow app
 * Author: Angel Ramboi <angel.ramboi@gmail.com>
 * More info: https://github.com/pbs/powwow
*/

__POWWOW_SITE_URL = '/'

if (typeof gapi != 'undefined'){
    gapi.hangout.onApiReady.add(function(eventObj){
        if (eventObj.isApiReady) {
            console.log('App loaded');
            confluence();
            jira();
            github();
        }
    });
} else {
    $(document).ready(function() {
        confluence();
        jira();
        github();
    });
}

function confluence(){
    var container = $('#confluence_container');
    $.ajax({
        url: __POWWOW_SITE_URL + 'confluence',
        dataType: 'html',
        success: function(data){
            container.html(data);
        }
    });
}

function confluence_save(form){
    var button = $(form).find('button.btn');
    button.text('Saving ...')
        .removeClass('btn-primary')
        .addClass('btn-warning');

    $.post(__POWWOW_SITE_URL + 'confluence', $(form).serialize(),
        function(data){
            button.text('Success')
                .removeClass('btn-warning')
                .addClass('btn-success');
            setTimeout('button_change_to_save()', 1500);
        }
    );
}

function button_change_to_save(){
    $('#confluence_form button.btn')
        .text('Save changes')
        .addClass('btn-primary')
        .removeClass('btn-success');
}

function jira(){
    var container = $('#jira_container');
    $.ajax({
        url: __POWWOW_SITE_URL + 'jira',
        dataType: 'html',
        success: function(data){
            container.html(data);
        }
    });
}

function github(){
    var container = $('#github_container');
    $.ajax({
        url: __POWWOW_SITE_URL + 'github',
        dataType: 'html',
        success: function(data){
            container.html(data);
        }
    });
}

