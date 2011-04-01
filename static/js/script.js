/*-- A jQuery version of the GeoRegistry clock
--*/

// if we want to pass some value as an option,
// we should set it in the page in "clockSetterOptions"
var clockSetterOptions = {
    //css selector of the destination of the clock
    destinationSpan: 'header .time-wrapper',
    //auto updater
    autoUpdate: true
};

var ClockSetter = (function($, _options, undefined){
    var defaultOptions = {
        officeOffset: 240,
        displayFormat: "Your Local Time: " +
                    "<span class='local-time'></span> on " +
                    "<span class='local-day'></span>",
        //update every second (1000 milliseconds)
        updateFrequency: 1000
    };
    var opts = $.extend(defaultOptions, _options);
    var visitorTime = new Date();
    var visitorOffset = new Date().getTimezoneOffset();
    var weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    var clockSpan, timeSpan, daySpan; //these are set later
    
    var _updateTimer; //this is used internally by updateLocalTime
    function updateLocalTime() {
        //this function should be callable from a timer and should
        //update the time in "clockSpan"
        visitorTime = new Date();
        
        if(!!timeSpan) {
            var h = visitorTime.getHours(),
                  m = visitorTime.getMinutes(),
                  s = visitorTime.getSeconds();
            timeSpan.text([h,
                (m < 10 ? '0' : '') + m,
                (s < 10 ? '0' : '') + s].join(':'));
        }
        
        if(!!daySpan) {
            var d = visitorTime.getDay();
            if(!daySpan.data('date-number') || daySpan.data('date-number')!==d) {
                //day will switch at midnight :)
                daySpan.data('date-number', d);
                daySpan.text(weekdays[d]);
            }
        }
        
        if(opts.autoUpdate) {
            //beware multiple simultaneous threads!
            window.clearTimeout(_updateTimer);
            _updateTimer = window.setTimeout(updateLocalTime, opts.updateFrequency);
        }
    }
    
    $(function startClock(){
        //This "startClock" is called when the whole document has loaded. (which is 
        //  generally a good time to call these kinds of things.)
        clockSpan = $(opts.destinationSpan).html(opts.displayFormat);
        timeSpan = $('.local-time', clockSpan);
        daySpan = $('.local-day', clockSpan);
        updateLocalTime();
        clockSpan.removeClass('hidden');
    });
    //only the returned value is accessible elsewhere in the page.
    return {
        offset: visitorOffset
    }
})(jQuery, clockSetterOptions);

/*--
var oldClockSetter = (function(){
    var officeoffset = 240;
    browser = (parseInt(navigator.appVersion) >= 4)
    var weekdays = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    if(! weekdays) { browser = 0; }
    if(browser) {
    var visitortime = new Date();
    var visitoroffset = visitortime.getTimezoneOffset();
    if(visitoroffset < 0) { visitoroffset = Math.abs(visitoroffset) + 720; }
    else { visitoroffset = 720 - visitoroffset; }
    if(officeoffset < 0) { officeoffset = Math.abs(officeoffset) + 720; }
    else { officeoffset = 720 - officeoffset; }
    var diff = officeoffset - visitoroffset;
    var officetime = new Date();
    officetime.setTime(Number(visitortime) + (diff * 60000));
    }

    // function to calculate local time
    // in a different city
    // given the city's UTC offset
    function calcTime(city, offset)
    {
    // create Date object for current location
    d = new Date();

    // convert to msec
    // add local time zone offset
    // get UTC time in msec
    utc = d.getTime() + (d.getTimezoneOffset() * 60000);

    // create new Date object for different city
    // using supplied offset
    nd = new Date(utc + (3600000*offset));

    // return time as a string
    return "The local time in " + city + " is " + nd.toLocaleString();
    }

    // get Bombay time
    (calcTime('Bombay', '+5.5'));

    // get Singapore time
    (calcTime('Singapore', '+8'));

    // get London time
    (calcTime('London', '+1'));
    
    var displayStr = "";
    function docWriteSim(str) {
        displayStr += str;
    }
    
    if(browser) {
    docWriteSim('<table><tr><td align="right">');
    docWriteSim("Your Local Time:</td><td><b>");
    docWriteSim(visitortime.getHours() + ':');
    if(visitortime.getMinutes() < 10) { docWriteSim('0'); }
    docWriteSim(visitortime.getMinutes()); 
    docWriteSim('</b> on ' + weekdays[visitortime.getDay()]);
    docWriteSim('</td></tr><tr><td align="right">');

    docWriteSim("Web site Business Office:</td><td><b>");
    docWriteSim(officetime.getHours() + ':');
    if(officetime.getMinutes() < 10) { docWriteSim('0'); }
    docWriteSim(officetime.getMinutes()); 
    docWriteSim('</b> on ' + weekdays[officetime.getDay()]);
    docWriteSim('</td></tr></table>');
    }
    
    
    if(browser)
        {
        docWriteSim("Your Local Time: ");
        docWriteSim(visitortime.getHours() + ':');

        if(visitortime.getMinutes() < 10) { docWriteSim('0'); }
        docWriteSim(visitortime.getMinutes());
        docWriteSim(' on ' + weekdays[visitortime.getDay()]);
        }

    console.log(displayStr);
    
    $("header p.time-wrapper").html(displayStr).removeClass('hidden');
//    $('body').append(displayStr);
});
   --*/