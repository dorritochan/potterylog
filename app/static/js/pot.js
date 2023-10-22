
$(document).ready(function() {

    Fancybox.bind("[data-fancybox='gallery']", {
        compact: false,
        contentClick: "iterateZoom",
        Images: {
            Panzoom: {
            maxScale: 2,
            },
        },
        Toolbar:{
            items: {
                delete: {
                    tpl: `<button class="f-button fancybox-button--delete" data-fancybox-delete id="btn-delete-image-fancybox"><i class="bi bi-trash3"></i></button>`,
                    click: () => {
                        var imgFullSrc = $('.fancybox__slide.has-image.is-selected img').attr('src');
                        var currentFancyboxLink = $(`a[data-fancybox="gallery"][href="${imgFullSrc}"]`)
                        var potId = currentFancyboxLink.data("pot-id");
                        set_confirm_modal_data_image_delete(imgFullSrc, potId);
                    }
                },
            },
            display: {
                left: ["infobar"],
                middle: [
                    "zoomIn",
                    "zoomOut",
                    "toggle1to1",
                    "rotateCCW",
                    "rotateCW",
                    "flipX",
                    "flipY",
                ],
                right: [
                    "slideshow",
                    "fullscreen",
                    "thumbs",
                    "delete",
                    "close",
                ],
            }
        },
        on: {
            init: function(instance) {
                console.log("Fancybox initialized!", instance);
            }
        }
    });

    $('[id^="sort-pot-"]').click(function() {
        var column = this.id.split("-").pop();
        console.log(column);

        var allIcons = $('[id^="sort-pot-"').find('i');

        var currentIcon = $(this).find('i');

        allIcons.each(function(index, element) {
        
            // For jQuery operations on the element, you can wrap it with $():
            var icon = $(element);

            // Skip the current icon
            if (icon.is(currentIcon)) {
                return;  // Continue to the next iteration
            }

            var iconClass = icon.attr('class');
            icon.removeClass(iconClass);
            icon.addClass('fa-solid fa-sort');
        
        });

        // Styling the current sorting icon
        var iconClasses = ["fa-solid fa-sort", "fa-solid fa-sort-up", "fa-solid fa-sort-down"];
        var currentIconClass = currentIcon.attr('class');
        currentIcon.removeClass(currentIconClass);
        var currentIconClassIndex = iconClasses.indexOf(currentIconClass);
        var nextIconClassIndex = currentIconClassIndex + 1;
        console.log(nextIconClassIndex);
        if (currentIconClassIndex == 2) {
            nextIconClassIndex = 0;
        }
        currentIcon.addClass(iconClasses[nextIconClassIndex]);

        $.ajax({
            type: 'GET',
            url: '/order_pots_by' + column + '/<asc_desc>',
            headers: {
                'X-CSRFToken': '{{ form.csrf_token._value() }}'
            },
            success: function(data) {
                
                
                // // Fetch the glaze choices and set them for the newly added field
                // $.get('/get_glaze_choices', function(choicesData) {
                //     var firstOption = [[0, '-']];
                //     var choices = firstOption.concat(choicesData);
                //     $('#glaze-field-' + glazeCount + ' select[name$="glaze"]').html(getOptionsHtml(choices));
                //     glazeCount++;
                // });

            }
        });
        
    });


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
        console.log("segment Count");
        console.log(segmentCount);
        var initialSegmentContent = $('#firing-segments').html();

        $('#add-segment').click(function() {
            addNewSegment(segmentCount);
            segmentCount++;
        });
    }


    $('#btn-add-glaze').click(function(event) {
        event.preventDefault(); // Prevent the form from reloading the page
        event.stopPropagation();

        // Get the index of the last glaze-field- element and populate the select
        // fields with updated glaze info in a loop
        var lastGlazeLayerId = $('[id^="glaze-field-"]').last().attr('id');
        var glazeLayerCount = parseInt(lastGlazeLayerId.split('-').pop(), 10);
        let selectedChoices = [];
        for (let index = 0; index <= glazeLayerCount; index++) {
            var select = $('#glaze-field-' + index + ' select[name$="glaze"]');
            selectedChoices.push(select.val());
        }

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
                        // update the list of glazes without a page reload on the edit/add pot page
                        $.get('/get_glaze_choices', function(choicesData) {
                            console.log
                            for (let index = 0; index <= glazeLayerCount; index++) {
                                var firstOption = [[0, '-']];
                                var choices = firstOption.concat(choicesData);
                                var select = $('#glaze-field-' + index + ' select[name$="glaze"]');
                                select.html(getOptionsHtml(choices));
                                select.val(selectedChoices[index]);
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

    //var initialSegmentContent = $('#firing-segments').html();

    // Reset the add/edit clay modal to the default - adding
    $('[id^="modal-add-edit-"]').on('hidden.bs.modal', function() {
        const itemType = $(this).data('itemtype');

        $("#form-add-edit-" + itemType)[0].reset();
        $(`#modal-add-edit-${itemType}-title`).text('Add a new ' + itemType);
        $(`#btn-add-${itemType}`).removeClass("hidden");
        $(`[id^="btn-update-${itemType}"]`).attr("id", `btn-update-${itemType}`);
        $(`[id^="btn-update-${itemType}"]`).addClass("hidden");
        $(`[id^="btn-delete-item-"][data-itemtype="${itemType}"]`).attr("id", "btn-delete-item-");
        $(`[id^="btn-delete-item-"][data-itemtype="${itemType}"]`).addClass("hidden");
        if (itemType == 'firing-program'){
            $('#firing-segments').html(initialSegmentContent);
            segmentCount = JSON.parse(segmentCountElement.attr('data-variable'));
        }
    });

    $('[id^="modal-confirm-delete"]').on('hidden.bs.modal', function() {
        $("[id^='btn-confirm-delete-item-']").attr("id", "btn-confirm-delete-item-")
    });

    $('#btn-add-clay').click(function(event) {
        event.preventDefault(); // Prevent the form from reloading the page
        event.stopPropagation();
        
        var select = $('#clay-field select[name$="clay"]');
        let selectedChoice = select.val();

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
                            
                            select.html(getOptionsHtml(choices));
                            select.val(selectedChoice);
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

                            // Check if the field is related to firing segments
                            if (itemType == 'firing-program') {
                                if (error.includes('Both start and end temperatures are required for the first segment.')) {
                                    $("#form-add-edit-" + itemType).find('[id="firing-segment-0"]').after(errorSpan);
                                }

                            } 
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
        console.log('Add firing program...');

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
                    console.log(response.errors);
                    $('#modal-add-edit-firing-program').modal('show');
                    // Clear previous errors
                    $(".form-error").remove();

                    // Loop through the errors and display them
                    $.each(response.errors, function(field, errors) {
                        // For each error of a field, create an error span
                        $.each(errors, function(_, error) {
                            var errorSpan = $("<span>").addClass("form-error").css("color", "red").text("[" + error + "]");

                            // Check if the field is related to firing segments
                            if (error.includes('Both start and end temperatures are required for the first segment.')) {
                                $("#form-add-edit-firing-program").find('[id="firing-segment-0"]').after(errorSpan);
                            }
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

    $("[id^='btn-delete-image']").click(function(event) {

        // Prevent default behavior
        event.preventDefault();
        // Stop event propagation
        event.stopPropagation();

        var imgFullSrc = $(this).data("image-src");
        var potId = parseInt($(this).data("pot-id"));

        console.log(imgFullSrc);
        console.log(potId);

        set_confirm_modal_data_image_delete(imgFullSrc, potId);

        
    });


    // This function acts on click on the confirm delete button in the confirm modal
    // and removes the item from the database. After that, the page is being refreshed.
    $("[id^='btn-confirm-delete-item-']").click(function() {
        
        // This is the type of item to be deleted, like 'pot' or 'link'
        var itemType = $(this).data("itemtype");
        
        if (itemType == 'image') {
            var imgSrc = $(this).attr('id').replace('btn-confirm-delete-item-', '');
            var potId = $(this).data("pot-id");
        } else {
            // Get the number from the ID
            var idNumber = parseInt(this.id.split("-").pop());
        }


        console.log(idNumber);
        console.log(itemType);
        console.log(imgSrc);
        console.log(potId);
        
        var url = ''
        if (itemType == 'image') {
            url = '/delete_image_from_pot/' + imgSrc + '/' + potId;
        } else {
            url = '/delete_' + itemType + '/' + idNumber;
        }

        fetch(url, { 
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


    $("[id^='open-modal-edit-item-']").click(async function() {
        var idNumber = parseInt(this.id.split("-").pop());
        var itemType = $(this).data("itemtype");

        try {
            const response = await fetch('/get_' + itemType + '/' + idNumber, { 
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            console.log('Item loaded:', data);
            
            if (itemType == 'firing-program') {
                segmentCount = data.number_of_segments;
                console.log("segment Count");
                console.log(segmentCount);
                for (let i = 1; i < segmentCount; i++) {
                    await addNewSegment(i)
                }
            }
            
            for (let key in data) {
                $(`#modal-add-edit-${itemType} input[id='${key}']`).val(data[key]);
                $(`#modal-add-edit-${itemType} select[id='${key}']`).val(data[key]).trigger('change');
                $(`#modal-add-edit-${itemType} textarea[id='${key}']`).val(data[key]);
                if (itemType == 'firing-program' && key != 'type' && key != 'number_of_segments') {
                    var segmentIndex = key.split('-').pop();
                    var $inputSegment = $(`#modal-add-edit-${itemType} div[id='firing-segments'] div[id='firing-segment-${segmentIndex}'] input[id='${key}']`);
                    // var $inputSegment1 = $(`#modal-add-edit-firing-program div[id='firing-segments'] div[id='firing-segment-0'] input[id='temp_start-0']`);
                    $inputSegment.val(data[key]);
                }
                fetch("/get_name_" + itemType + "/" + idNumber)
                .then(response => response.json())
                .then(data => {
                    const titleText = 'Edit ' + itemType.replace("-", " ") + ' ' + data.item_name;
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

        } catch(error) {
                console.log('There was a problem with the get operation:', error.message);
            };
    });

    // This function opens the Edit pot page on click on a pot row on Index page
    $('[id^="row-pot-"]').click(function() {
        var potId = parseInt(this.id.split('-').pop());
        window.location.href = '/editpot/' + potId;
    });


    // This function navigates to the index page on click on the Cancel button when adding a pot
    $('[id="btn-cancel-add-pot"]').click(function() {
        window.location.href = '/index'
    });

    

});


function getOptionsHtml(choices) {
    var optionsHtml = '';
    for (var i = 0; i < choices.length; i++) {
        optionsHtml += '<option value="' + choices[i][0] + '">' + choices[i][1] + '</option>';
    }
    return optionsHtml;
}

function addNewSegment(segmentCount) {
    return $.ajax({  // return the jqXHR object (which is "thenable", or a promise-like object)
        type: 'GET',
        url: '/get_segment/' + segmentCount,
        headers: {
            'X-CSRFToken': '{{ form.csrf_token._value() }}'
        },
        success: function(data) {
            console.log('success');
            $('#firing-segments').append(data);
        }
    });
}

function set_confirm_modal_data_image_delete(imgFullSrc, potId) {


    var imgSrc = '';
    // var encodedImgSrc = encodeURIComponent(imgFullSrc);
    $.get('/image_name/', { image_source: imgFullSrc }, function(response) {
        imgSrc = response.item_name;
    }).fail(function() {
        console.error("Error fetching image name.");
    });

    console.log(imgSrc);

    // Fetch the item's name using AJAX
    $.get('/get_name_pot/' + potId, function(response) {
    

        // Update the modal's content with the fetched data
        $('#modal-confirm-delete-title').text('Confirm image deletion');
        $('#txt-question-confirm-delete').html('Do you really want to delete the image <strong>' + imgSrc + '</strong> from the pot ' + response.item_name + '?');
        var $btnDelete = $("[id^='btn-confirm-delete-item-']")
        $btnDelete.attr("id", $btnDelete.attr("id") + imgSrc)
        $btnDelete.data('itemtype', 'image');
        $btnDelete.data('pot-id', potId);

        // Show the image
        $('#image-confirm-modal').attr("src", imgFullSrc);
        $('#image-confirm-modal').attr("alt", imgFullSrc);
        $('#image-container-confirm-modal').removeClass("hidden");

        // Show the modal
        $('#modal-confirm-delete').modal('show');
    });
}


