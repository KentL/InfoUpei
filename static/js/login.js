/**
 * Created by zhuol_000 on 2015/9/9.
 */
$(document).ready(function() {
    // When login page loading,check if the "login as student" or "login as staff" button is checked,
    // Then enable the corresponding textbox pair and disable the other pair
    if($("#student_type_radio_btn").is(":checked"))
    {
        $("#student_username_txt").attr("disabled",false);
        $("#student_password_txt").attr("disabled",false);
        $("#staff_username_txt").attr("disabled",true);
        $("#staff_password_txt").attr("disabled",true);
    }

    if($("#staff_type_radio_btn").is(":checked"))
    {
        $("#student_username_txt").attr("disabled",true);
        $("#student_password_txt").attr("disabled",true);
        $("#staff_username_txt").attr("disabled",false);
        $("#staff_password_txt").attr("disabled",false);
    }


    //******************Radio button on-click methods****************//
    //When either one of the radio button is clicked, enable the corresponding textbox pair
    // and disable the other pair
    $("#student_type_radio_btn").click(function(){
        $("#student_username_txt").attr("disabled",false);
        $("#student_password_txt").attr("disabled",false);
        $("#staff_username_txt").attr("disabled",true);
        $("#staff_password_txt").attr("disabled",true);
        });

    $("#staff_type_radio_btn").click(function() {
        $("#student_username_txt").attr("disabled", true);
        $("#student_password_txt").attr("disabled", true);
        $("#staff_username_txt").attr("disabled", false);
        $("#staff_password_txt").attr("disabled", false);
    });
    //************************************************************//

});


