if(jQuery) (function(jQuery) {
    jQuery(document).ready(function() {
        if(jQuery().socialSharePrivacy && $('.socialshareprivacy').length > 0) {

            var social_media_buttons = [];
            $.ajax({
              async: false,
              url: '/@@kotti_blog_social_media_buttons',
              success: function(response) {
                  social_media_buttons = response['social_media_buttons'];
              }
            });

            var kotti_blog_services = {
                facebook: {
                    'status':         'on',
                    'dummy_img':      '',
                    'txt_info':       '2 Klicks f&uuml;r mehr Datenschutz: Erst wenn Sie hier klicken, wird der Button aktiv und Sie k&ouml;nnen Ihre Empfehlung an Facebook senden. Schon beim Aktivieren werden Daten an Dritte &uuml;bertragen &ndash; siehe <em>i</em>.',
                    'txt_fb_off':     'nicht mit Facebook verbunden',
                    'txt_fb_on':      'mit Facebook verbunden',
                    'perma_option':   'on',
                    'display_name':   'Facebook',
                    'referrer_track': '',
                    'language':       'de_DE',
                    'action':         'recommend',
                    'dummy_caption':  'Empfehlen'
                },
                twitter:  {
                    'status':          'on',
                    'dummy_img':       '',
                    'txt_info':        '2 Klicks f&uuml;r mehr Datenschutz: Erst wenn Sie hier klicken, wird der Button aktiv und Sie k&ouml;nnen Ihre Empfehlung an Twitter senden. Schon beim Aktivieren werden Daten an Dritte &uuml;bertragen &ndash; siehe <em>i</em>.',
                    'txt_twitter_off': 'nicht mit Twitter verbunden',
                    'txt_twitter_on':  'mit Twitter verbunden',
                    'perma_option':    'on',
                    'display_name':    'Twitter',
                    'referrer_track':  '',
                    'language':        'en',
                    'dummy_caption':   'Tweet'
                },
                gplus:    {
                    'status':         'on',
                    'dummy_img':      '',
                    'txt_info':       '2 Klicks f&uuml;r mehr Datenschutz: Erst wenn Sie hier klicken, wird der Button aktiv und Sie k&ouml;nnen Ihre Empfehlung an Google+ senden. Schon beim Aktivieren werden Daten an Dritte &uuml;bertragen &ndash; siehe <em>i</em>.',
                    'txt_gplus_off':  'nicht mit Google+ verbunden',
                    'txt_gplus_on':   'mit Google+ verbunden',
                    'perma_option':   'on',
                    'display_name':   'Google+',
                    'referrer_track': '',
                    'language':       'de'
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
                services: kotti_blog_services,
                'css_path' : ''
            });
        }
    });
})(jQuery);
