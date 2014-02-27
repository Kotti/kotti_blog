// English translations for https://github.com/patrickheck/socialshareprivacy
// taken from http://c5demo.patrickheck.de/.

if(jQuery) (function(jQuery) {
  jQuery(document).ready(function($) {
    if( jQuery().socialSharePrivacy && $('.socialshareprivacy').length > 0) {

      var social_media_buttons = [];
      $.ajax({
          async: false,
          url: '/@@kotti_blog_social_media_buttons',
          success: function(response) {
              social_media_buttons = response['social_media_buttons'];
          }
      });

      var kotti_blog_services = {
        facebook : {
          'status'    : 'on',
          'txt_info'    : '2 clicks for increased privacy: Only after clicking here the button will become active and allow connecting to Facebook. Data will already be transferred upon activation &ndash; see <em>i</em>',
          'txt_fb_off'  : 'not connected to Facebook',
          'txt_fb_on'   : 'connected to Facebook',
          'display_name'  : 'Facebook',
          'language'    : 'en_US',
          'action'    : 'like',
          'dummy_caption' : 'Like'
        },
        twitter : {
          'status'      : 'on',
          'txt_info'     : '2 clicks for increased privacy: Only after clicking here the button will become active and allow connecting to Twitter. Data will already be transferred upon activation &ndash; see <em>i</em>',
          'txt_twitter_off'   : 'not connected to twitter',
          'txt_twitter_on'  : 'connected to twitter',
          'display_name'    : 'Twitter',
          'language'      : 'en',
          'dummy_caption'   : 'Tweet'
        },
        gplus : {
          'status'      : 'on',
          'txt_info'    : '2 clicks for increased privacy: Only after clicking here the button will become active and allow connecting to Google+. Data will already be transferred upon activation &ndash; see <em>i</em>',
          'txt_glus_off'  : 'not connected to google+',
          'txt_gplus_on'  : 'connected to google+',
          'display_name'  : 'Google+',
          'language'    : 'en'
        }
      };

      if ($.inArray('facebook', social_media_buttons) == -1) {
        kotti_blog_services['facebook']['status'] = 'off';
      }
      if ($.inArray('twitter', social_media_buttons) == -1) {
        kotti_blog_services['twitter']['status'] = 'off';
      }
      if ($.inArray('google', social_media_buttons) == -1) {
        kotti_blog_services['gplus']['status'] = 'off';
      }

      $('.socialshareprivacy').socialSharePrivacy({
        services : kotti_blog_services,
        'info_link' : 'http://www.heise.de/ct/artikel/2-Klicks-fuer-mehr-Datenschutz-1333879.html',
        'txt_help' : 'If you activate these buttons, data will be transferred to Facebook, Twitter or Google in the USA. This data might also be stored there. For further information click the <em>i</em> button."',
        'settings_perma' : 'Activate permanently and confirm transfer of data:',
        'css_path' : ''
      });
    }
  });
})(jQuery);

