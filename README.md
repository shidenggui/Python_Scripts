# Python_Scripts
平时写的一些Python脚本

## tushareweb
用flask写的tushareweb服务器，可以调用tushare返回json数据

调用方式: `localhost/tushare?func=函数名&参数1=值1&参数2=值2`

例: `tushare?func=get_hist_data&code=000001`

## tusharetosql
抓取tushare日线数据到mysql
