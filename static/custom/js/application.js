$('#processAIRequestForm').on('submit', function (e) {
    e.preventDefault();

    $('#response').val();
    $('#sources').val();

    $.ajax({
        url: this.action,
        type: this.method,
        contentType: 'application/json',
        data: JSON.stringify({user_query: $('#user_query').val()}),
        success: function (data) {
            console.log(data);
            if (data?.answer) {
                $('#response').val(data.answer);
            } else {
                $('#response').val(data.error);
            }

            if (data?.sources) {
                $('#sources').val(data.sources);
            } else {
                $('#sources').val();
            }
        },
        error: function (response) {
            let errors = response?.responseJSON?.detail;
            if (Array.isArray(errors) === false) {
                errors = [{msg: errors}];
            }
            let msg = errors.map(function (error) {
                return error.msg;
            }).join(', ');
            alert('Errors: ' + msg);
        }
    });
});
