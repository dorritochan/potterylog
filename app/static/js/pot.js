
$(document).ready(function() {
    var glazeCount = JSON.parse($('#glaze-count').attr('data-variable'));
    console.log("Script is loaded!");
    console.log(glazeCount)
    $('#add-glaze-layer').click(function() {
        $.ajax({
            type: 'GET',
            url: '/get_glaze_field/' + glazeCount,
            headers: {
                'X-CSRFToken': '{{ form.csrf_token._value() }}'
            },
            success: function(data) {
                $('#glaze-fields').append(data);
                
                // Fetch the glaze choices and set them for the newly added field
                $.get('/get_glaze_choices', function(choicesData) {
                    var firstOption = [[-1, '-']];
                    var choices = firstOption.concat(choicesData);
                    $('#glaze-field-' + glazeCount + ' select[name$="glaze"]').html(getOptionsHtml(choices));
                    glazeCount++;
                });

            }
        });
    });
});

function getOptionsHtml(choices) {
    var optionsHtml = '';
    for (var i = 0; i < choices.length; i++) {
        optionsHtml += '<option value="' + choices[i][0] + '">' + choices[i][1] + '</option>';
    }
    return optionsHtml;
}