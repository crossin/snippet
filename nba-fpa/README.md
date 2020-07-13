## NBA球员出手点绘制

#### 运行环境
- Python 3.6

#### 运行依赖包
- requests
- matplotlib
- pandas

#### 代码说明
1. 用户ID需手动输入，可从 https://stats.nba.com/players/ 这里查找
2. 蓝色点为命中，红色点为未命中
3. 建议通过 Jupyter 运行，效果会比较好。py文件运行有可能在某些系统出现错位
4. 最初版本的NBA API已失效，有2个替代方案：
   1. 使用别人下载好的数据：https://github.com/toddwschneider/nba-shots-db
   2. 一个付费API服务：https://probasketballapi.com/docs/shotcharts 可以免费试用一周，拿来做个练习足够（但部分球员部分赛季数据有缺失）

#### 参考文章

[【圆老司】用python展示NBA球员出手位置偏好（含新数据接口）](https://www.bilibili.com/read/cv6752561)

[NBA的球星们喜欢在哪个位置出手](https://mp.weixin.qq.com/s/pumsu5IVpb3P5BSycBC1mA)

#### 演示效果

![JamesHarden.png](JamesHarden.png)

![StephenCurry.png](StephenCurry.png)

![DeMarDeRozan.png](DeMarDeRozan.png)

![GiannisAntetokounmpo.png](GiannisAntetokounmpo.png)

![JeremyLin.png](JeremyLin.png)

要是喜欢就关注下我的公众号呗，“**Crossin的编程教室**”，或者同名 [知乎专栏](https://zhuanlan.zhihu.com/crossin)

里面还有很多有意思的程序，感谢各位！

![crossincode](../crossin-logo.png)