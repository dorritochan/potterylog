
$(document).ready(function() {
    var glazeCountElement = $('#glaze-count');
    if (glazeCountElement.length) {
        var glazeCount = JSON.parse(glazeCountElement.attr('data-variable'));
        console.log("Script is loaded!");
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
                        var firstOption = [[0, '-']];
                        var choices = firstOption.concat(choicesData);
                        $('#glaze-field-' + glazeCount + ' select[name$="glaze"]').html(getOptionsHtml(choices));
                        glazeCount++;
                    });

                }
            });
        });
    }


    var segmentCountElement = $('#segment-count');
    if (segmentCountElement.length){
        var segmentCount = JSON.parse(segmentCountElement.attr('data-variable'));
        console.log("Script is loaded!");
        $('#add-segment').click(function() {
            console.log("Click!");
            $.ajax({
                type: 'GET',
                url: '/get_segment/' + segmentCount,
                headers: {
                    'X-CSRFToken': '{{ form.csrf_token._value() }}'
                },
                success: function(data) {
                    console.log('success');
                    console.log(data);
                    $('#firing-segments').append(data);
                    segmentCount++;
                }
            });
        });
    }


    $('#btn-add-glaze').click(function(event) {
        event.preventDefault(); // Prevent the form from reloading the page
        event.stopPropagation();

        $.ajax({
            url: "/addglaze",
            type: "POST",
            data: $('#form-add-glaze').serialize(),
            success: function(response) {
                if (response.success) {
                    // Close the modal and update the pot info, if necessary
                    $('#modal-add-glaze').modal('hide');
                    var shouldReload = $('#add-new-glaze').data('reload-page');
                    if (shouldReload) {
                        location.reload();
                    } else {
                        // update the list of glazes without a page reload
                        $.get('/get_glaze_choices', function(choicesData) {
                            var firstOption = [[0, '-']];
                            var choices = firstOption.concat(choicesData);
                            
                            var lastGlazeLayerId = $('[id^="glaze-field-"]').last().attr('id');
                            var glazeLayerCount = parseInt(lastGlazeLayerId.split('-').pop(), 10);
                            console.log(glazeLayerCount);
                            for (let index = 0; index <= glazeLayerCount; index++) {
                                $('#glaze-field-' + index + ' select[name$="glaze"]').html(getOptionsHtml(choices));
                            }
                        });
                    }
                } else {
                    $('#modal-add-glaze').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-glaze").find('[name="' + field + '"]').after(errorSpan);
                        });
                    });
                }
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

function updateGlazeList() {
    $.ajax({
        url: "/get_updated_glaze_list",
        type: "GET",
        success: function(data) {
            // Assuming 'data' contains the updated list of glazes
            // Update the DOM with the new list
            $("#glaze-list").html(data);
        }
    });
}
