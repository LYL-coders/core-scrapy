**记录ajax中的请求。**

AJAX ：异步 JavaScript 和 XML

1. 是一种用于创建快速动态网页的技术。 

2. 通过在后台与服务器进行少量数据交换，AJAX 可以使网页实现异步更新。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新。 

AJAX = Asynchronous JavaScript and XML，翻译为：异步的 JavaScript 和 XML。ajax就是基于浏览器提供的XMLHttpRequest对象来实现的。

传统的网页(不使用 AJAX)如果需要更新内容，必需重载整个网页面。自从有了ajax之后，我们就可以实现异步的加载网页。

什么叫异步？

异步，异嘛，不同的意思，这里也就是指不跟浏览器加载执行网页代码的步伐一致，也就是说在一个网页中需要用户操作来触发执行代码，而不是整个网页代码一次性执行完毕。(这里的用户操作是指在同一个网页下面请求代码执行渲染，而不是让浏览器直接跳转渲染另一个页面)



AJAX 工作原理：

这里面都提到了一个概念XML，那什么是XML呢？

XML 指可扩展标记语言(eXtensible Markup Language)。

我们在浏览器中使用XMLHTTPRequest对象在服务器之间通信，传输的数据是使用XML的方式，但最终还是会被转换成json数据格式来被我们使用。

我们再来看看XHR的使用流程：首先我们需要新建一个XMLHttpRequest实例

var xhr = new XMLHttpRequest();然后，向远程主机发出一个HTTP请求

xhr.open('GET', 'example.php');

xhr.send();接着，就等待远程主机做出回应。这时需要监控XMLHttpRequest对象的状态变化，指定回调函数

xhr.onreadystatechange = function(){

if ( xhr.readyState == 4 && xhr.status == 200 ) {

alert( xhr.responseText );

} else {

alert( xhr.statusText );

}

};上面的代码包含了老版本XMLHttpRequest对象的主要属性：

* xhr.readyState：XMLHttpRequest对象的状态，等于4表示数据已经接收完毕。

* xhr.status：服务器返回的状态码，等于200表示一切正常。

* xhr.responseText：服务器返回的文本数据

* xhr.responseXML：服务器返回的XML格式的数据

* xhr.statusText：服务器返回的状态文本。

老版本的XMLHttpRequest对象有以下几个缺点：* 只支持文本数据的传送，无法用来读取和上传二进制文件。

* 传送和接收数据时，没有进度信息，只能提示有没有完成。

* 受到"同域限制"(Same Origin Policy)，只能向同一域名的服务器请求数据。

以上都是2010年以前使用的出来的过时的XMLHttpRequest对象了，现在我们都基本上使用的是HTML5中的新版本XMLHttpRequest对象。

新版本的功能：

新版本的XMLHttpRequest对象，针对老版本的缺点，做出了大幅改进。* 可以设置HTTP请求的时限。

* 可以使用FormData对象管理表单数据。

* 可以上传文件。

* 可以请求不同域名下的数据(跨域请求)，CORS。

* 可以获取服务器端的二进制数据。

* 可以获得数据传输的进度信息。

1】HTTP请求的时限

xhr.timeout = 3000;

xhr.ontimeout = function(event){

alert('请求超时！');

}

上面的语句，将最长等待时间设为3000毫秒。过了这个时限，就自动停止HTTP请求。与之配套的还有一个timeout事件，用来指定回调函数。

2】FormData对象

ajax操作往往用来传递表单数据。为了方便表单处理，HTML 5新增了一个FormData对象，可以模拟表单。

//首先，新建一个FormData对象。var formData = new FormData();

//然后，为它添加表单项。formData.append('username', '张三');

formData.append('id', 123456);

//最后，直接传送这个FormData对象。这与提交网页表单的效果，完全一样。xhr.send(formData);

FormData对象也可以用来获取网页表单的值：

var form = document.getElementById('myform');

var formData = new FormData(form);

formData.append('secret', '123456'); // 添加一个表单项xhr.open('POST', form.action);

xhr.send(formData);

3】上传文件

新版XMLHttpRequest对象，不仅可以发送文本信息，还可以上传文件。

假定files是一个"选择文件"的表单元素(input[type="file"])，我们将它装入FormData对象。

var formData = new FormData();

for (var i = 0; i < files.length;i++) {

formData.append('files[]', files[i]);

}

xhr.send(formData);

4】跨域资源共享(CORS)

新版本的XMLHttpRequest对象，可以向不同域名的服务器发出HTTP请求。这叫做"跨域资源共享"(Cross-origin resource sharing，简称CORS)。

使用"跨域资源共享"的前提，是浏览器必须支持这个功能，而且服务器端必须同意这种"跨域"。如果能够满足上面的条件，则代码的写法与不跨域的请求完全一样。

跨域之前我们都讲过了，这里就不多提了，其他的新XMLHttpRequest对象的功能，个人觉得日常开发中可能遇到很少，就不去总结了。
相关资源：Linux下以C构建WEB服务同时响应XHR(XMLHttpRequest)请求_javaweb...
————————————————
版权声明：本文为CSDN博主「weixin_39774491」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/weixin_39774491/article/details/111855598