
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
                            // Get the index of the last glaze-field- element and populate the select
                            // fields with updated glaze info in a loop
                            var lastGlazeLayerId = $('[id^="glaze-field-"]').last().attr('id');
                            var glazeLayerCount = parseInt(lastGlazeLayerId.split('-').pop(), 10);
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
    

    $('#btn-add-clay').click(function(event) {
        event.preventDefault(); // Prevent the form from reloading the page
        event.stopPropagation();

        $.ajax({
            url: "/addclay",
            type: "POST",
            data: $('#form-add-clay').serialize(),
            success: function(response) {
                if (response.success) {
                    // Close the modal and update the pot info, if necessary
                    $('#modal-add-clay').modal('hide');
                    var shouldReload = $('#add-new-clay').data('reload-page');
                    if (shouldReload) {
                        location.reload();
                    } else {
                        // update the list of glazes without a page reload
                        $.get('/get_clay_choices', function(choicesData) {
                            var firstOption = [[0, '-']];
                            var choices = firstOption.concat(choicesData);
                            
                            $('#clay-field select[name$="clay"]').html(getOptionsHtml(choices));
                        });
                    }
                } else {
                    $('#modal-add-clay').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-clay").find('[name="' + field + '"]').after(errorSpan);
                        });
                    });
                }
            }
        });
    });

    $('#btn-add-kiln').click(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();

        $.ajax({
            url: "/addkiln",
            method: "POST",
            data: $('#form-add-kiln').serialize(),
            success: function(response) {
                if (response.success) {
                    $('#modal-add-kiln').modal('hide');
                    var shouldReload = $('#add-new-kiln').data('reload-page');
                    if (shouldReload) {
                        location.reload();
                    }
                } else {
                    $('#modal-add-kiln').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-kiln").find('[name="' + field + '"]').after(errorSpan);
                        });
                    });
                }
            }
        });
    });


    $('#btn-add-firing-program').click(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();

        $.ajax({
            url: "/addfiringprogram",
            method: "POST",
            data: $('#form-add-firing-program').serialize(),
            success: function(response) {
                if (response.success) {
                    $('#modal-add-firing-program').modal('hide');
                    var shouldReload = $('#add-new-firing-program').data('reload-page');
                    if (shouldReload) {
                        location.reload();
                    }
                } else {
                    $('#modal-add-firing-program').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-firing-program").find('[name="' + field + '"]').after(errorSpan);
                        });
                    });
                }
            }
        });
    });

    $('#btn-add-link').click(function(event) {
        event.preventDefault();
        event.stopImmediatePropagation();

        $.ajax({
            url: "/addlink",
            method: "POST",
            data: $('#form-add-link').serialize(),
            success: function(response) {
                if (response.success) {
                    $('#modal-add-link').modal('hide');
                    location.reload();
                } else {
                    $('#modal-add-link').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-link").find('[name="' + field + '"]').after(errorSpan);
                        });
                    });
                }
            }
        });
    });
    

    $("[id^='btn-delete-link-']").click(function() {
        // Get the number from the ID
        var idNumber = parseInt(this.id.split("-").pop());
    
        fetch('/deletelink/' + idNumber, { // Assuming 123 is the ID of the item you want to delete
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            // Include other headers as needed (e.g., authentication tokens)
        }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            console.log('Item deleted:', data);
            location.reload();
        })
        .catch(error => {
            console.log('There was a problem with the delete operation:', error.message);
        });

        console.log(idNumber);
    });

});


function getOptionsHtml(choices) {
    var optionsHtml = '';
    for (var i = 0; i < choices.length; i++) {
        optionsHtml += '<option value="' + choices[i][0] + '">' + choices[i][1] + '</option>';
    }
    return optionsHtml;
}

