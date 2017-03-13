# -*- coding=utf-8 -*-

import re
import time
import logging

import http


class nexusphp():
    def __init__(self, host, https):
        self.host = host
        if https:
            self.http = 'https://'
        else:
            self.http = 'http://'
        self.index_url = self.http + self.host
        self.user_url = None
        
        self.signin_date = None

        self.cookie = http.get_cookie(host)
        if not self.cookie:
            raise Exception('get_cookie fail')

    def init(self):
        '''
            get user details page URL from index page:
            #<span class="nowrap"><a href="userdetails.php?id=44370" style="color:#" class=\'User_Name\'><b>hackqiang</b></a></span>
        '''
        index_page = http.get_page(self.cookie, self.index_url)
        
        #logging.debug(index_page)
        
        match = re.search('(userdetails\.php\?id=\d+)', index_page)
        if match:
            self.user_url = self.http + self.host + '/' + match.group()
    
    def signin(self):
    
        date = time.strftime('%Y%m%d', time.localtime())
        if date == self.signin_date:
            logging.info('%s already sign in today' % self.host)
            #return True
        
        self.signin_date = date
        
        signin_url = ''
        signin_data = None
        
        if self.host == 'hdhome.org' or self.host == 'www.hdpter.net':
            '''
            hdhome.org
                <a href="attendance.php" class="faqlink">簽到得魔力</a>
            '''
            signin_url = self.http + self.host + '/attendance.php'

        elif self.host == 'pt.upxin.net':
            '''
            https://pt.upxin.net/
                <font style=" font-weight: bold; color:red">  &nbsp&nbsp&nbsp<span id="qiandao"><a href="#" onclick="javascript:qiandao('qiandao')">[签到]</a></span><span id="yiqiandao" style="display: none;">[已签到]</span></font> 签到次数：1
                function qiandao(action)
                {
                    var list=ajax.post('added.php',function(msg){ 
                    document.getElementById( "qiandao" ).style.display = "none";
                    document.getElementById( "yiqiandao" ).style.display = "inline";
                    document.getElementById("mybounus").innerHTML = document.getElementById("mybounus").innerHTML+" 签到奖励：<span style='color: rgb(255, 0, 0);'>"+msg+"</span>";
                    alert("你还需要继续努力哦！此次签到，你获得了魔力奖励："+msg);
                    },'action='+action);
                }
                --> POST added.php with action=qiandao
            '''
            signin_data = {'action':'qiandao'}
            signin_url = self.http + self.host + '/added.php'

        elif self.host == 'www.hyperay.org':
            '''
            https://www.hyperay.cc/
                <span id="sign_in"><a href="#" onclick="javascript:sign_in('sign_in')"><font color="red">[签到]</font></a></span><span id="sign_in_done" style="display: none;"><font color="green">[已签到]</font></span></font>&nbsp;(1) 
                function sign_in(action)
                {var list=ajax.post('sign_in.php',function(msg){document.getElementById("sign_in").style.display="none";document.getElementById("sign_in_done").style.display="inline";alert(msg);},'action='+action);}
                --> POST sign_in.php with action=sign_in
            '''
            signin_data = {'action':'sign_in'}
            signin_url = self.http + self.host + '/sign_in.php'

        elif self.host == 'totheglory.im':
            #  $(document).ready(function(){
            #    $("a#signed").click(function(){
            #        $.post("signed.php", {signed_timestamp: "1488303012", signed_token: "f7bb2f00bc9e1397c5cac4cc7ebebc03"}, function(data) {
            #            $('#sp_signed').html("<b style=\"color:green;\">已签到</b>");
            #            alert(data);
            #        });
            #    });
            #  $(document).ready(function(){
            #    $("a#signed").click(function(){
            #        $.post("signed.php", {signed_timestamp: "1488303401", signed_token: "01c8905a20d01ea482aed5460363ed43"}, function(data) {
            #            $('#sp_signed').html("<b style=\"color:green;\">已签到</b>");
            #            alert(data);
            #        });
            #    });

            pass

        else:
            logging.error('%s not support sign in' % self.host)
            return False
        
        html = http.get_page(self.cookie, signin_url, signin_data)
        # logging.debug(html)
        
        if not html:
            logging.error('sign in %s error' % signin_url)
            self.signin_date = None
            return False

        return True
        
    def search(self, keywords):
        url = self.http + self.host + '/torrents.php'

        if self.host == 'hdcmct.org':
            params = 'incldead=1&spstate=0&inclbookmarked=0&search=%s&search_area=0&search_mode=0' % keywords
        elif self.host == 'www.hdpter.net':
            params = 'incldead=1&spstate=0&picktype=0&inclbookmarked=0&search=%s&search_area=0&search_mode=0' % keywords
        else:
            params = 'incldead=1&spstate=0&pick=0&inclbookmarked=0&search=%s&search_area=0&search_mode=0' % keywords

        request_url = '%s?%s' % (url, params)
        html = http.get_page(self.cookie, request_url)
        logging.debug(html)
        return html
        
    def get_user_info(self):
        '''
            return
                (True, upload_siz, download_size, coin)
                or
                (False, '', '', '')
                
        '''
        if not self.user_url:
            self.init()
            
        if self.user_url:
            user_page = http.get_page(self.cookie, self.user_url)
            
            #logging.debug(user_page)
            
            '''
                <td class="embedded"><strong>上传量</strong>: 114.801 GiB</td><td class="embedded"><strong>下载量</strong>: 0 B</td></tr><tr><td class="embedded"><strong>实际上传</strong>: 64.544 GiB</td><td class="embedded"><strong>实际下载</strong>: 779.242 GiB</td>
                <td class="embedded"><strong>上傳量</strong>: 312.69 GB</td><td class="embedded"><strong>下載量</strong>: 22.03 GB</td>
                <td class="embedded"><strong>上传量</strong>: 38.70 GB (本月: 38.70 GB)</td><td class="embedded"><strong>下载量</strong>: 10.44 GB (本月: 10.44 GB)</td></tr><tr><td class="embedded"><strong>实际上传量</strong>: 30.81 GB (本月: 30.81 GB)</td><td class="embedded"><strong>实际下载量</strong>: 132.07 GB (本月: 132.07 GB
                <td class="embedded"><strong>上传量</strong>: 29.70 GB</td><td class="embedded"><strong>下载量</strong>: 0.00 KB</td>    
                <td class="embedded"><strong>上传量</strong>: 4.95 GB</td><td class="embedded"><strong>下载量</strong>: 0.00 KB</td>
                <td class="embedded"><strong>上傳量</strong>: 635.57 GB</td><td class="embedded"><strong>下載量</strong>: 0.00 KB</td>
                
                <strong>上传量</strong>(显/虚/实):  89.60GB&nbsp;/&nbsp;0.00KB&nbsp;/&nbsp;42.30GB</td></tr><tr><td class="embedded"><strong>下载量</strong>(显/虚/实):  0.00KB&nbsp;/&nbsp;0.00KB&nbsp;/&nbsp;0.00KB
                
                <font class='color_uploaded'>上传量:</font>89.60GB<font class='color_downloaded'>下载量:</font>0.00KB	<font class=
                
                <font color=green>上传量 : </font> <font color=black><a href="#" onclick="return false;" title="139,517.91 MB">136.25 GB</a></font>&nbsp;&nbsp;<font color=darkred>下载量 :</font> <font color=black><a href="#" onclick="return false;" title="42,185.18 MB">41.20 GB</a></font>
                
            '''
            # match = re.search('(<td class="embedded"><strong>.*B</td>)', user_page)
            
            if not user_page:
                return False, '', '', ''
            
            user_page = user_page.replace('&nbsp;', '')
            
            upload = 'unknow'
            match = re.search('<td class="embedded"><strong>上传量</strong>: (.*?B).*</td><td class="embedded"><strong>下载量</strong>', user_page)
            if match:
                upload = match.groups()[0]
            
            if upload == 'unknow':
                match = re.search('<td class="embedded"><strong>上傳量</strong>: (.*?B).*</td><td class="embedded"><strong>下載量</strong>', user_page)
                if match:
                    upload = match.groups()[0]

            if upload == 'unknow':
                match = re.search('<font class=\'color_uploaded\'>上传量:</font>(.*?B)<font', user_page)
                if match:
                    upload = match.groups()[0]
                    
            if upload == 'unknow':
                match = re.search('上传量 : </font> <font color=black><a href="#" onclick="return false;" title=".*B">(.*?B)</a>', user_page)
                if match:
                    upload = match.groups()[0]

            download = 'unknow'
            match = re.search('</td><td class="embedded"><strong>下载量</strong>: (.*?B).*</td>', user_page)
            if match:
                download = match.groups()[0]
            
            if download == 'unknow':
                match = re.search('</td><td class="embedded"><strong>下載量</strong>: (.*?B).*</td>', user_page)
                if match:
                    download = match.groups()[0]

            if download == 'unknow':
                match = re.search('<font class=\'color_downloaded\'>下载量:</font>(.*?B).*<font class=', user_page)
                if match:
                    download = match.groups()[0]
                    
            if download == 'unknow':
                match = re.search('<font color=darkred>下载量 :</font> <font color=black><a href="#" onclick="return false;" title=".*B">(.*?B).*</a></font>', user_page)
                if match:
                    download = match.groups()[0]
                    
            '''
                <td width="99%" class="rowfollow" valign="top" align="left"><strong>魔力值:</strong> 789.2 <b>做种积分:</b> 789.2 (本月: 789.2)<br /><br /><small>注：做种积分自2014年1月1日零时开始统计</small></td>
                <td width="1%" class="rowhead nowrap" valign="top" align="right">魔力值</td><td width="99%" class="rowfollow" valign="top" align="left">25708.8</td>
                <td width="1%" class="rowhead nowrap" valign="top" align="right">魔力值</td><td width="99%" class="rowfollow" valign="top" align="left">123<a href='myhistory.php?id=5690' class='faqlink'>查看魔力值、账户历史</a></td>
                <td width="1%" class="rowhead nowrap" valign="top" align="right">魔力</td><td width="99%" class="rowfollow" valign="top" align="left">528&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<a href='myhistory.php?id=331' class='faqlink'>查看魔力、账户历史</a></td></tr>
                <td width="1%" class="rowhead nowrap" valign="top" align="right">魔力值</td><td width="99%" class="rowfollow" valign="top" align="left">152.2</td>
                <td width="1%" class="rowhead nowrap" valign="top" align="right">魔力值</td><td width="99%" class="rowfollow" valign="top" align="left">84537.3</td>
                <td width="1%" class="rowhead nowrap" valign="top" align="right">魔力值</td><td width="99%" class="rowfollow" valign="top" align="left">75.1</td>
                <td width="1%" class="rowhead nowrap" valign="top" align="right">魔力值</td><td width="99%" class="rowfollow" valign="top" align="left">196.5</td>
                <td width="1%" class="rowhead nowrap" valign="top" align="right">UCoin<br />[<a href="ucoin.php?id=44370" class="faqlink">详情</a>]</td><td width="99%" class="rowfollow" valign="top" align="left"><span class="ucoin-notation"><span class="ucoin-symbol ucoin-gold">9</span><span class="ucoin-symbol ucoin-silver">61</span><span class="ucoin-symbol ucoin-copper">46</span></span><br />(96,146.724)</td>
                
                积分 : <a href="/mybonus.php">7030.12</a><a href="/mall.php">
            '''
            coin = 'unknow'
            match = re.search('<td width="1%" class="rowhead nowrap" valign="top" align="right">魔力.*?</td><td width="99%" class="rowfollow" valign="top" align="left">(.*?)<', user_page)
            if match:
                if match.groups():
                    coin = match.groups()[0]
            
            if coin == 'unknow':
                # for U2
                match = re.search('<span class="ucoin-symbol ucoin-copper">\d*</span></span><br />\((.*)\)</td>', user_page)
                if match:
                    if match.groups():
                        coin = match.groups()[0]
            
            if coin == 'unknow':
                # for CMCT
                match = re.search('<td width="99%" class="rowfollow" valign="top" align="left"><strong>魔力值:</strong> (.*) <b>', user_page)
                if match:
                    if match.groups():
                        coin = match.groups()[0]
                        
            if coin == 'unknow':
                # for TTG
                match = re.search('积分 : <a href="/mybonus.php">(.*)</a><a href="/mall.php">', user_page)
                if match:
                    if match.groups():
                        coin = match.groups()[0]

            return True, upload.strip(), download.strip(), coin.replace(',', '').strip()
        
        return False, '', '', ''
