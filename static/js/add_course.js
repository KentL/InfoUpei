$(document).ready(function() {
    var course_description_type=$("#course_form input:radio[name=course_description]:checked").val();
    if(course_description_type=='txt')
    {
        $("#course_form input[name=course_description_file]").attr("disabled", true);
        $("#course_form textarea[name=course_description_text]").attr("disabled", false);
    }
    if(course_description_type=='file')
    {
        $("#course_form input[name=course_description_file]").attr("disabled", false);
        $("#course_form textarea[name=course_description_text]").attr("disabled", true);
    }
    if(course_description_type=='none')
    {
        $("#course_form input[name=course_description_file]").attr("disabled", true);
        $("#course_form textarea[name=course_description_text]").attr("disabled", true);
    }

    //Disable other course description field when one radio button is clicked
    $("#course_form input:radio[name=course_description]").click(function(){
            course_description_type=$("#course_form input:radio[name=course_description]:checked").val();
            if(course_description_type=='txt')
            {
                $("#course_form input[name=course_description_file]").attr("disabled", true);
                $("#course_form textarea[name=course_description_text]").attr("disabled", false);
            }
            if(course_description_type=='file')
            {
                $("#course_form input[name=course_description_file]").attr("disabled", false);
                $("#course_form textarea[name=course_description_text]").attr("disabled", true);
            }
            if(course_description_type=='none')
            {
                $("#course_form input[name=course_description_file]").attr("disabled", true);
                $("#course_form textarea[name=course_description_text]").attr("disabled", true);
            }
        });
});