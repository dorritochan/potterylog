
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
            data: $('#form-add-edit-glaze').serialize(),
            success: function(response) {
                if (response.success) {
                    // Close the modal and update the pot info, if necessary
                    $('#modal-add-edit-glaze').modal('hide');
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
                    $('#modal-add-edit-glaze').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-edit-glaze").find('[name="' + field + '"]').after(errorSpan);
                        });
                    });
                }
            }
        });
    });

    // Reset the add/edit clay modal to the default - adding
    $('[id^="modal-add-edit-"]').on('hidden.bs.modal', function() {
        const itemType = $(this).data('itemtype');
        console.log('Were in there');
        console.log(itemType);

        $("#form-add-edit-" + itemType)[0].reset();
        $(`#modal-add-edit-${itemType}-title`).text('Add a new ' + itemType);
        $(`#btn-add-${itemType}`).removeClass("hidden");
        $(`[id^="btn-update-${itemType}"]`).attr("id", `btn-update-${itemType}`);
        $(`[id^="btn-update-${itemType}"]`).addClass("hidden");
        $(`[id^="btn-delete-item-"][data-itemtype="${itemType}"]`).attr("id", "btn-delete-item-");
        $(`[id^="btn-delete-item-"][data-itemtype="${itemType}"]`).addClass("hidden");
    });

    $('[id^="modal-confirm-delete"]').on('hidden.bs.modal', function() {
        $("[id^='btn-confirm-delete-item-']").attr("id", "btn-confirm-delete-item-")
    });

    $('#btn-add-clay').click(function(event) {
        event.preventDefault(); // Prevent the form from reloading the page
        event.stopPropagation();

        $.ajax({
            url: "/addclay",
            type: "POST",
            data: $('#form-add-edit-clay').serialize(),
            success: function(response) {
                if (response.success) {
                    // Close the modal and update the pot info, if necessary
                    $('#modal-add-edit-clay').modal('hide');
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
                    $('#modal-add-edit-clay').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-edit-clay").find('[name="' + field + '"]').after(errorSpan);
                        });
                    });
                }
            }
        });
    });

    $('[id^="btn-update-"]').click(function(event) {
        var idNumber = parseInt(this.id.split("-").pop());
        var itemType = $(this).data("itemtype");

        console.log(idNumber);
        console.log(itemType);

        $.ajax({
            url: "/update_" + itemType + "/" + idNumber,
            type: "PUT",
            data: $('#form-add-edit-' + itemType).serialize(),
            success: function(response) {
                if (response.success) {
                    console.log('success');
                    // Close the modal and update the pot info, if necessary
                    $('#modal-add-edit-' + itemType).modal('hide');
                    var shouldReload = $('[id^="open-modal-edit-item-"]').data('reload-page');
                    if (shouldReload) {
                        location.reload();
                    } 
                } else {
                    console.log('failure');
                    console.log(response);
                    $('#modal-add-edit-' + itemType).modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-edit-" + itemType).find('[name="' + field + '"]').after(errorSpan);
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
            data: $('#form-add-edit-kiln').serialize(),
            success: function(response) {
                if (response.success) {
                    $('#modal-add-edit-kiln').modal('hide');
                    var shouldReload = $('#add-new-kiln').data('reload-page');
                    if (shouldReload) {
                        location.reload();
                    }
                } else {
                    $('#modal-add-edit-kiln').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-edit-kiln").find('[name="' + field + '"]').after(errorSpan);
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
            data: $('#form-add-edit-firing-program').serialize(),
            success: function(response) {
                if (response.success) {
                    $('#modal-add-edit-firing-program').modal('hide');
                    var shouldReload = $('#add-new-firing-program').data('reload-page');
                    if (shouldReload) {
                        location.reload();
                    }
                } else {
                    $('#modal-add-edit-firing-program').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-edit-firing-program").find('[name="' + field + '"]').after(errorSpan);
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
            data: $('#form-add-edit-link').serialize(),
            success: function(response) {
                if (response.success) {
                    $('#modal-add-edit-link').modal('hide');
                    location.reload();
                } else {
                    $('#modal-add-edit-link').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");
                            // Append errorSpan next to the respective input field
                            $("#form-add-edit-link").find('[name="' + field + '"]').after(errorSpan);
                        });
                    });
                }
            }
        });
    });

    // This function gets the name of the item (clay, link, glaze,...)
    // after the button Delete was clicked and opens the delete confirmation 
    // modal with the correct title
    $("[id^='btn-delete-item-']").click(function() {
        var idNumber = parseInt(this.id.split("-").pop());
        var itemType = $(this).data("itemtype");

        console.log(idNumber);
        console.log(itemType);

        // Fetch the item's name using AJAX
        $.get('/get_name_' + itemType + '/' + idNumber, function(response) {
        

        // Hide the modal for editing if it was open
        if ($(`#modal-add-edit-${itemType}`).hasClass('show')) {
            $(`#modal-add-edit-${itemType}`).modal('hide');
        }

        // Update the modal's content with the fetched data
        $('#modal-confirm-delete-title').text('Confirm ' + itemType + ' deletion');
        $('#txt-question-confirm-delete').html('Do you really want to delete the ' + itemType + ' <strong>' + response.item_name + '</strong>?');
        var $btnDelete = $("[id^='btn-confirm-delete-item-']")
        $btnDelete.attr("id", $btnDelete.attr("id") + idNumber)
        $btnDelete.data('itemtype', itemType);

        // Show the modal
        $('#modal-confirm-delete').modal('show');
    });


    });

    // This function acts on click on the confirm delete button in the confirm modal
    // and removes the item from the database. After that, the page is being refreshed.
    $("[id^='btn-confirm-delete-item-']").click(function() {
        // Get the number from the ID
        var idNumber = parseInt(this.id.split("-").pop());

        // This is the type of item to be deleted, like 'pot' or 'link'
        var itemType = $(this).data("itemtype");

        console.log(idNumber);
        console.log(itemType);
    
        fetch('/delete_' + itemType + '/' + idNumber, { 
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
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

    });

    // This ensures manual controls and not automatic sliding of the carousel
    $('#photo-carousel').carousel({
        interval: false 
    });

    // A click function on a photo thumbnail on Edit pot page opens
    // the carousel and shows the clicked photo.
    $("[id^='photo-thumbnail-']").click(function() {
        var indexPhoto = parseInt(this.id.split("-").pop());
        console.log('clicked on thumbnail');

        // Go to the clicked slide
        $('#photo-carousel-modal').on('shown.bs.modal', function () {
            $('#photo-carousel').carousel(indexPhoto);
        });

        $('#photo-carousel-modal').modal('show');


    });


    $("[id^='open-modal-edit-item-']").click(function() {
        var idNumber = parseInt(this.id.split("-").pop());
        console.log(idNumber);
        var itemType = $(this).data("itemtype");
        console.log(itemType);

        fetch('/get_' + itemType + '/' + idNumber, { 
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Item loaded:', data);
                for (let key in data) {
                    $(`#modal-add-edit-${itemType} input[id='${key}']`).val(data[key]);
                    $(`#modal-add-edit-${itemType} select[id='${key}'] option:contains('${data[key]}')`).prop('selected', true).parent().trigger('change');
                    $(`#modal-add-edit-${itemType} textarea[id='${key}']`).val(data[key]);
                    fetch("/get_name_" + itemType + "/" + idNumber)
                        .then(response => response.json())
                        .then(data => {
                            const titleText = 'Edit ' + itemType + ' ' + data.item_name;
                            $(`#modal-add-edit-${itemType}-title`).text(titleText);
                        })
                        .catch(error => console.error('Error fetching name:', error));
                }
                $('#btn-add-' + itemType).addClass("hidden");

                var $btnUpdate = $('#btn-update-' + itemType);
                $btnUpdate.attr('value', 'Update ' + itemType);
                $btnUpdate.attr('id', 'btn-update-' + itemType + '-' + idNumber)
                $btnUpdate.removeClass("hidden");

                var $btnDelete = $(`[id^="btn-delete-item-"][data-itemtype="${itemType}"]`);
                $btnDelete.attr("id", $btnDelete.attr("id") + idNumber)
                $btnDelete.removeClass("hidden");
                
                $('#modal-add-edit-' + itemType).show('modal');
            })
            .catch(error => {
                console.log('There was a problem with the get operation:', error.message);
            });
    });

    // This function opens the Edit pot page on click on a pot row on Index page
    $('[id^="row-pot-"]').click(function() {
        var potId = parseInt(this.id.split('-').pop());
        window.location.href = '/editpot/' + potId;
    });

    

});


function getOptionsHtml(choices) {
    var optionsHtml = '';
    for (var i = 0; i < choices.length; i++) {
        optionsHtml += '<option value="' + choices[i][0] + '">' + choices[i][1] + '</option>';
    }
    return optionsHtml;
}



