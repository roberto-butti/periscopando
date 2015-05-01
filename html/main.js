// Enable pusher logging - don't include this in production
Pusher.log = function(message) {
  if (window.console && window.console.log) {
    window.console.log(message);
  }
};

var pusher = new Pusher(pusher_app_key);
var channel = pusher.subscribe('test_channel');
channel.bind('my_event', function(data) {
  var source   = $("#entry-template").html();
  var template = Handlebars.compile(source);
  $( "#content" ).prepend(template(data));
 //   "<tr><td>"+data.username+"</td><td>"+data.text+"</td><td><a href='"+data.url+"'>View on Periscope</td><td>Who: "+data.username+"</td><td><img src='"+data.profile_image+"'></td><td>Language:"+data.lang+"</td><td>From:"+data.timezone+"</td></tr>");
});










