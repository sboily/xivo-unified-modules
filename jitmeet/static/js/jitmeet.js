$('body').on('hidden.bs.modal', '#jitmeet-invite', function () {
    $(this).removeData('bs.modal');
});

$('body').on('show.bs.modal', '#jitmeet-invite', function (e) {
    $('.modal-body').load(e.relatedTarget.dataset.url);
});

$('.modal-footer #commit').click(function() {
    url = $('textarea#email').data('url');
    $.ajax({ type:'POST',
             url: url,
             data:$('#form-invite').serialize(),
           });
});
