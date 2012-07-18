if(jQuery) (function(jQuery) {
    jQuery(document).ready(function() {
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
    });
})(jQuery);
