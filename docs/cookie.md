# 如何获取cookie

1. 用Chrome打开<https://passport.weibo.cn/signin/login>；
2. 输入微博的用户名、密码，登录，如图所示：
![weibo log in page](https://picture.cognize.me/cognize/github/weibospider/cookie1.png)
登录成功后会跳转到<https://m.weibo.cn>;
3. 按F12键打开Chrome开发者工具，在地址栏输入并跳转到<https://weibo.cn>，跳转后会显示如下类似界面:
![chrome debugger network tab](https://picture.cognize.me/cognize/github/weibospider/cookie2.png)
4. 依此点击Chrome开发者工具中的Network->Name中的weibo.cn->Headers->Request Headers，"Cookie:"后的值即为我们要找的cookie值，复制即可，如图所示：
![cookie in request headers section](https://picture.cognize.me/cognize/github/weibospider/cookie3.png)
5. 我的cookie：SUB=_2A25JTXehDeRhGeFL61YX-C7FyD-IHXVqzhnprDV6PUJbkdANLWitkW1NQo4LyoUPFTd4-Yi8jp4XxtiiZPto9e3m; SCF=AmR9KXAT8hg73O9EnBd0xbCI31CiHKmXK-8z94ek70pwDqiQsswzTzatI2kfDANRGz-cLgLmPIM3Fb4QI8yYYy8.; SSOLoginState=1682507761; _T_WM=82175302422; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=luicode=20000174&uicode=20000174