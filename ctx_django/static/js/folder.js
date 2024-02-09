$(function(){
    //返回上一级
    $("#back-button").click(function () {
        location.href = $("#goback").text()
    })
    // 新建文件夹
    $("#create").click(function () {
        $("#folder_input").show();
        $("#folder_name").focus()
    })
    $("#cancel-create").click(function () {
        $("#folder_input").hide();
    })
    // 文件夹名称验证
    $("#create-button").click(function () {
        var folder_name = $("#folder_name").val()
        if (folder_name === ""){
            alert("请输入文件名")
        }
        else {
             if(! space_detect(folder_name)){
                $("#create-form").submit();
                }
            else {
                alert("文件夹名称不能包含空格，请重新输入。")
            }
        }
    })
    // 文件上传
    $("#upload").click(function(){
        $("#file_upload").click();
    })
    $("#file_upload").change(function(){
        $('#progress').show()
        var files = $("#file_upload")[0].files;
        for(i=0,len=files.length;i<len;i++){
            files[i].name = files[i].name.replace(/\s+/g, '#')
        }
        var form = new FormData(document.getElementById('upload_form'))
        var xhr = new XMLHttpRequest();
        var url = $("#upload_form").attr("action")
        xhr.upload.addEventListener('progress',on_progress,false);
        xhr.open('POST',url,true);
        xhr.setRequestHeader('X-CSRFTOKEN',$("[name='csrfmiddlewaretoken']")[0].value);
        xhr.send(form);
     })

    // 文件与文件夹选项
    $('.folder-detail').mouseenter(function(){
        $(this).find(".hidden-option").show();
    });
    $(".folder-detail").mouseleave(function(){
        $(this).find(".hidden-option").hide();
    });
    // 点击重命名按钮
    $(".rename-button").click(function(){
        var input_form = $(this).parent().siblings(".rename-form");
        var item_name = $(this).parent().siblings("a.name").children(".item-name");
        input_form.show();
        input_form.children(":text").attr("placeholder",item_name.text())
        input_form.children(":text").focus();
        $(this).parent().hide();
    });
    // 重命名提交确认
    $(".rename-form :submit").click(function () {
        var new_name = $(this).siblings("input[name='new_name']").val()
        var name = $(this).parent().siblings("a.name").children(".item-name").text()
        if(space_detect(new_name)){
            alert("名称中不能含有空格");
            return false;
        }
        if(new_name===get_prefix(name)){
            alert("请输入新的文件名");
            return false;
        }
    })
    // 取消重命名
    $(".rename-form :button").click(function(){
        $(this).parent().hide();
        $(this).parent().siblings(".name").children(".item-name").show();
        $(this).parent().siblings(".hidden-option").show();
    });
    // 鼠标移出取消重命名
     $(".rename-form").mouseleave(function () {
        $(this).find(":button").click();
     })
    // 文件删除确认
    $(".del-button").click(function(){
    var url = $(this).siblings(".del-url").text();
    if (confirm("确定要删除吗？")){
        var form = new FormData()
        var xhr = new XMLHttpRequest();
        xhr.open('POST',url,true);
        xhr.setRequestHeader('X-CSRFTOKEN',$("[name='csrfmiddlewaretoken']")[0].value);
        xhr.send(form);
        }
    location.reload()
    })
    //图片视频预览
    /*可以从服务器读取字节流
    $(function () {
        var img = $(".image-icon")
        var url = img.attr('src')
        var xmlhttp = new XMLHttpRequest()
            xmlhttp.open("POST",url,true);
            xmlhttp.responseType = "blob";
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
    })*/
})

function space_detect(text,target=" ") {
    if(text.indexOf(target) !== -1){
        return true
    }
}

function get_prefix(filename) {
    var prefix = filename;
    if(space_detect(filename,".")){
        prefix = filename.substring(0, filename.lastIndexOf("."));
    }
    return prefix
}

function on_progress(evt) {
    if(evt.lengthComputable) {
        var ele = document.getElementById('progress-finish');
        var percent = Math.round((evt.loaded) * 100 / evt.total);
        ele.style.width = percent + '%';
        document.getElementById('progress-rate').innerHTML = percent + '%';
        if(percent === 100){location.reload()};
    }
}