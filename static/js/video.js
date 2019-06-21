//访问用户媒体设备的兼容方法
    function getUserMedia(constraints, success, error) {
      if (navigator.mediaDevices.getUserMedia) {
        //最新的标准API
        navigator.mediaDevices.getUserMedia(constraints).then(success).catch(error);
      } else if (navigator.webkitGetUserMedia) {
        //webkit核心浏览器
        navigator.webkitGetUserMedia(constraints,success, error)
      } else if (navigator.mozGetUserMedia) {
        //firfox浏览器
        navigator.mozGetUserMedia(constraints, success, error);
      } else if (navigator.getUserMedia) {
        //旧版API
        navigator.getUserMedia(constraints, success, error);
      }
    }



           //从 canvas 提取图片 image 
      function convertCanvasToImage(canvas) { 
        //新Image对象，可以理解为DOM 
        var image = new Image(); 
        // canvas.toDataURL 返回的是一串Base64编码的URL
        // 指定格式 PNG 
        image.src = canvas.toDataURL("image/png");
        return image.src;
      } 
 

    let video = document.getElementById('video');
    let canvas = document.getElementById('canvas');
    let context = canvas.getContext('2d');

    function success(stream) {
      //兼容webkit核心浏览器
      let CompatibleURL = window.URL || window.webkitURL;
      //将视频流设置为video元素的源
      console.log(stream);

      //video.src = CompatibleURL.createObjectURL(stream);
      video.srcObject = stream;
      video.play();
    }

    function error(error) {
      console.log(`访问用户媒体设备失败${error.name}, ${error.message}`);
    }

    if (navigator.mediaDevices.getUserMedia || navigator.getUserMedia || navigator.webkitGetUserMedia || navigator.mozGetUserMedia) {
      //调用用户媒体设备, 访问摄像头
      getUserMedia({video : {width: 480, height: 320}}, success, error);
    } else {
      alert('不支持访问用户媒体');
    }

    document.getElementById('capture').addEventListener('click', function () {
      context.drawImage(video, 0, 0, 480, 320); 
      var imager = convertCanvasToImage(canvas);
               console.log(imager);
      // $('.panel-body').append(img)

       $.ajax({
        url: "http://127.0.0.1:5000/index",
        data: {
            users_img: imager
        },
        success: function (data) {
            console.log(data)
            }
        });
        $(window).attr('location','/sign_date');
    });

