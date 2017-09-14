$('.inbox-messages').on('click','a',function(e){
  that = $(this)
  if (that.attr('class') == "pm-delete") {
    e.preventDefault();
    delete_message();
  }

  function delete_message(){
    $.ajax({
      url  : that.attr('href').slice(0,16)+that.attr('href').slice(20,that.attr('href').length - 1),
      type : "DELETE",
      beforeSend: function (xhr) {
        xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
      },
      success : function(json) {
        document.getElementById('inbox-message-'+json.pk).remove()
      }
    })
  }
})

$('.reply-button').on('click',function(e){
  e.preventDefault();
  var that = $(this)
  var replyButtonId = that.attr('id').slice(13,that.attr('id').length)
  that.parent().addClass('hidden')
  that.parent().parent().append("<form id='reply-form-"+replyButtonId+"' class='reply-message' method='post'><div class='cm2'><input id='reply-subject-"+replyButtonId+"' class='form-control' type='text' placeholder='subject' value=''></div><div class='form-group'><textarea id='reply-message-"+replyButtonId+"' class='form-control' rows='4' placeholder='message' value=''></textarea></div><input type='submit' value='message' name='submit'><button class='cancelmessage'>cancel</button></form>")
})

$('.email-button').on('click',function(e){
  e.preventDefault();
  var that = $(this)
  var emailButtonId = that.attr('id').slice(13,that.attr('id').length)
  that.parent().addClass('hidden')
  that.parent().parent().append("<form id='email-form-"+emailButtonId+"' class='email-message' method='post'><div class='col-md-2'><input id='email-subject-"+emailButtonId+"' class='form-control' type='text' placeholder='subject' value=''></div><div class='form-group'><textarea id='email-message-"+emailButtonId+"' class='form-control' rows='4' placeholder='message' value=''></textarea></div><input type='submit' value='send email' name='submit'><button class='cancelmessage'>cancel</button></form>")
})

$('.text-button').on('click', function(e){
  e.preventDefault();
  var that = $(this)
  var textId = that.attr('id').slice(12,that.attr('id').length)
  var contactList = document.getElementById('inbox-options-'+textId)
  contactList.classList.add('hidden')
  that.parent().parent().append("<form id='text-form-"+textId+"' class='text-message' method='post'><div class='form-group'><textarea id='text-message-"+textId+"' class='form-control' rows='4' placeholder='message' value=''></textarea></div><input type='submit' value='send text' name='submit'><button class='cancelmessage'>cancel</button></form>")
})
