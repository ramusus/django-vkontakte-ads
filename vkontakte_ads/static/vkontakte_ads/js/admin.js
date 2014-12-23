var $ = django.jQuery;

$(function() {
    var fieldBidToggle = function() {
        $('#id_cost_type').change(function() {
            if($(this).val() === '0') {
                $('.field-cpm').hide();
                $('.field-cpc').show();
            } else if($(this).val() === '1') {
                $('.field-cpm').show();
                $('.field-cpc').hide();
            } else {
                $('.field-cpc,.field-cpm').show();
            }
        }).change();
    }();

    var targetingStats = function() {

        $('#targeting-0 .inline_label').after('&nbsp;<span id="targetingAudience"></span>');
        $('.field-cpc p.help').prepend('<strong id="targetingCpc"></strong>');
        $('.field-cpm p.help').prepend('<strong id="targetingCpm"></strong>');

        var targeting_fields = [
            'sex',
            'age_from',
            'age_to',
            'birthday',
            'country',
            'cities',
            'cities_not',
            'statuses',
            'group_types',
            'groups',
            'religions',
            'interests',
            'travellers',
            'districts',
            'stations',
            'streets',
            'schools',
            'positions',
            'school_from',
            'school_to',
            'uni_from',
            'uni_to',
            'browsers',
            'tags'
        ];

        var updateTargeting = function() {
            var ad_new = !document.location.href.match(/\/ad\/(\d+)\/$/);
            var targeting = {
                'account_id': $('#id_account').val(),
                'layout__link_url': $('#id_layout-0-link_url').val(),
                'layout__link_domain': $('#id_layout-0-link_domain').val() || 'vk.com',
            };

            if(!targeting['account_id'] && ad_new || !targeting['layout__link_url']) {
                return;
            }

            $.each(targeting_fields, function(i, field) {
                var jField = $('#id_targeting-0-' + field);
                var value = jField.val();
                if(jField.is('select[multiple]')) {
                    value = value ? value.join(',') : '';
                } else if(jField.is('input:checkbox')) {
                    value = jField.is(':checked') ? 1 : '';
                }
                targeting['targeting__' + field] = value;
            });

            $.ajax({
                url: 'targeting_stats/',
                type: 'post',
                data: targeting,
                dataType: 'json',
                beforeSend: function() {
                    var loader = '<img src="/static/vkontakte_ads/img/loading-indicator.gif">';
                    $('#targetingAudience,#targetingCpc,#targetingCpm').prepend(loader);
                },
                success: function(response) {
                    $('#targetingAudience').html('Целевая аудитория – ' + response.audience_count + ' человек');
                    $('#targetingCpc').html('Рекомендованное значение — ' + response.recommended_cpc + ' коп. ');
                    $('#targetingCpm').html('Рекомендованное значение — ' + response.recommended_cpm + ' коп. ');
                }
            });
        }

        $.each(targeting_fields, function(i, field) {
            $('#id_targeting-0-' + field).change(updateTargeting);
        });
        $.each(['link_url','link_domain'], function(i, field) {
            $('#id_layout-0-' + field).change(updateTargeting);
        });

        updateTargeting();

    }();

});