/* Author: 
    Sean Dunn
*/

(function($) {
    $("input").on("keypress", function(event) {
        if(event.keyCode === 13) {
            // For now, just unhide the div
            // Eventually, make a websocket call to the server
            this.value = "";
            $("#bayes").fadeIn("normal");
        }
    });
})(jQuery);
