// Theme custom js methods
$(document).ready(function(){

  var addYearSelectorCustomLabels = function(){
    var str2017 = {
      'es': 'prorrogado',
      'ca': 'prorrogat'
    };
    console.log('foo');

    $('.data-controllers .layout-slider .slider .slider-tick-label').each(function(){
      var val = $(this).html();
      if (val === '2017'){
        $(this).html(val + '<br/><small><i> ('+ str2017[ $('html').attr('lang') ] +')</i></small>');
      }
    });
  };

  addYearSelectorCustomLabels();
});
