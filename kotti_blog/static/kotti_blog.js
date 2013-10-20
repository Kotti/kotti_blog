if(jQuery) (function(jQuery) {
    jQuery(document).ready(function() {
        var use_auto_pagination = true;
        $.ajax({
            async: false,
            url: '/@@kotti_blog_use_auto_pagination',
            success: function(response) {
                use_auto_pagination = response['use_auto_pagination'];
            }
        });
        if(use_auto_pagination) {
            jQuery.ias({
                container : '.blogentries',
                item: '.blogentry',
                pagination: '.pagination',
                next: '.next a',
                loader: '<img src="/static-kotti_blog/loader.gif" />',
                onRenderComplete: function(items) {
                    if (jQuery.isFunction(jQuery.fn.ias_on_render_complete)) {
                        jQuery.fn.ias_on_render_complete();
                    }
                }
            });
        }
    });
})(jQuery);
