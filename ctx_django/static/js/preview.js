//加载图片
$(function () {
    var url = $("#url").text()
    if(document.getElementById('image')){
            var img = $("#image")
                var xmlhttp = new XMLHttpRequest()
                    xmlhttp.open("GET",url,true);
                    xmlhttp.responseType = "blob";
                    xmlhttp.send()
                    xmlhttp.onload = function(){
                        if (this.status == 200) {
                            var blob = this.response;
                            //var img = document.createElement("img");
                            img.onload = function(e) {
                                window.URL.revokeObjectURL(img.attr("src"));
                            };

                            img.attr("src", window.URL.createObjectURL(blob));
                        }
                    }
        }

    if(document.getElementById('video')){
        var video = $("#video")
        var xmlhttp = new XMLHttpRequest()
        xmlhttp.open("GET",url,true);
        xmlhttp.responseType = "blob";
        xmlhttp.send()
        xmlhttp.onload = function(){
            if (this.status == 200) {
                var blob = this.response;
                //var img = document.createElement("img");
                video.onload = function(e) {
                    window.URL.revokeObjectURL(video.attr("src"));
                };
                video.attr("src", window.URL.createObjectURL(blob));
            }
        }
    }
})
