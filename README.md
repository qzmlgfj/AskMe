# AskMe

为了追随早已远去的潮流，写个匿名提问箱。

## 尚在开发中

这是一个应该在毕业前就完成的项目，但一直拖到了现在。

## 现已上线

1.0版本现已发布，可使用`Gunicorn`进行部署

`gunicorn -b 127.0.0.1:5000 -D --log-file "./askme.log" "ask_me:create_app()"`

构建已于Pypi发布，可直接下载安装

`$ pip install ask_me`
