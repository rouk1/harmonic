(function ($, SimpleMDE) {
  $(document).ready(function () {
    $('.simple-mde-editor').each(function () {
      var e = new SimpleMDE({
        element: this,
        status: false,
        spellChecker: false
      })
      e.value($(this.id).val())
    })
  })
})(window.django.jQuery, window.SimpleMDE)
