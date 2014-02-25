if(jQuery) (function(jQuery) {
    jQuery(document).ready(function() {
        if(jQuery().socialSharePrivacy && $('.socialshareprivacy').length > 0) {
            $('.socialshareprivacy').socialSharePrivacy({
                'css_path' : ''
            });
        }
    });
})(jQuery);
