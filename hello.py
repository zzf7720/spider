from bs4 import BeautifulSoup

text = '''
  <div class="header">
  <div class="header-inner">
          <a href="//maoyan.com" class="logo" data-act="icon-click"></a>
        <div class="city-container" data-val="{currentcityid:1035 }">
            <div class="city-selected">
                <div class="city-name">
                  道县
                  <span class="caret"></span>
                </div>
            </div>
            <div class="city-list" data-val="{ localcityid: 1035 }">
                <div class="city-list-header">定位城市：<a class="js-geo-city" data-ci="1035">道县</a></div>

            </div>
        </div>


        <div class="nav">
            <ul class="navbar">
                <li><a href="/" data-act="home-click"  >首页</a></li>
                <li><a href="/films" data-act="movies-click" >电影</a></li>
                <li><a href="/cinemas" data-act="cinemas-click" >影院</a></li>
                <li><a href="http://www.gewara.com">演出</a></li>

                <li><a href="/board" data-act="board-click"  class="active" >榜单</a></li>
                <li><a href="/news" data-act="hotNews-click" >热点</a></li>
                <li><a href="/edimall"  >商城</a></li>
            </ul>
        </div>

        <div class="user-info">
            <div class="user-avatar J-login">
              <img src="https://p0.meituan.net/movie/7dd82a16316ab32c8359debdb04396ef2897.png">
              <span class="caret"></span>
              <ul class="user-menu no-login-menu">
                <li><a href="javascript:void 0">登录</a></li>
              </ul>
            </div>
        </div>

        <form action="/query" target="_blank" class="search-form" data-actform="search-click">
            <input name="kw" class="search" type="search" maxlength="32" placeholder="找影视剧、影人、影院" autocomplete="off">
            <input class="submit" type="submit" value="">
        </form>

        <div class="app-download">
          <a href="/app" target="_blank">
            <span class="iphone-icon"></span>
            <span class="apptext">APP下载</span>
            <span class="caret"></span>
            <div class="download-icon">
                <p class="down-title">扫码下载APP</p>
                <p class='down-content'>选座更优惠</p>
            </div>
          </a>
        </div>

  </div>
</div>
'''
import re
soup = BeautifulSoup(text,'lxml')

# result=soup.find(class_='navbar').find_all('li')
print(soup.find('ul').li.a.string)
# for i in result:
#     print(i.find('a').string)
# for i,child in enumerate(soup.ul.children):
#     print(i,child)
