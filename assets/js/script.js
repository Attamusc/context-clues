/* Author: 
    Sean Dunn
*/

(function($) {
    $("input").on("keypress", function(event) {
        if(event.keyCode === 13) {
            var self = this;
            // For now, just unhide the div
            // Eventually, make a websocket call to the server
            $("#bayes").html("<h2>Pay no attention to the man behind the curtain...</h2>");
            $("#bayes").fadeIn("normal");
            $.get("/OpenGraphQuery",
                {"query": $.trim(this.value) },
                function(data) {
                    self.value = '';
                    console.log(data);
                    $("#bayes").html(data);
                }
            );
        }
    });
})(jQuery);
