# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
from scrapy import Selector

dd = u"""
<div class="content_wrappr_left article article_16"><div class="content"><div class="BSHARE_POP blkContainerSblkCon clearfix blkContainerSblkCon_16" id="artibody"><p>　　新浪科技讯 11月10日上午消息，11月9日，美国华盛顿州当地高等法院召开听证会。新浪科技查询发现，法官在关于禁令的判决文书原文是“原告已经展示，这份顾颖琼公布的信托文件较有可能是伪造的，上面的签名并不是<a class="wt_article_link" onmouseover="WeiboCard.show(1999607273,'tech',this)" href="?zw=tech" target="_blank">贾跃亭</a>的。” 因此法庭批准了贾跃亭提出的初步禁令，对顾颖琼下达了未来24小时内删除关于贾跃亭的微信公众号等网络文章，不得在网上评论贾跃亭等命令。</p><p>　　听证会上，华盛顿州当地高等法院当庭再对顾颖琼发布预防性禁令（preliminary injunction），有效期截至2018年2月1日。据悉，美国法院下发的禁令包含临时禁令、预防性禁令。</p><p>　　乐视方面则称，听证会上，华盛顿州当地高等法院根据原告贾跃亭代理律师提供的证据，认为该证据证明了顾颖琼自2017年7月15日以来刊发的《独家解密 | 贾跃亭正在美国做的两件事》、《独家揭秘 | 带你走进贾跃亭在美国的家》、《贾跃亭 | 在美国不能乱说话,被发现可是要罚款坐牢的》、《贾跃亭洛杉矶地产数目接近美国总统》等10多篇文章中涉及贾跃亭的内容失实。</p><p>　　而顾颖琼表示，“我已经给中国韭菜们做了我能做的了，现在我需要专注处理好这个案件，这个案件还没有结束，有可能会一个旷日持久。“</p><p>　　今年7月以来，顾颖琼在个人自媒体“顾颖琼博士说天下”发布了关于贾跃亭的众多重磅爆料，其中包括贾跃亭为女儿在美国成立5亿海外信托基金的消息。</p><p>　　10月6日，洛杉矶高等法院正式受理了贾跃亭对顾颖琼提出的诽谤诉讼。10月9日，加州洛杉矶高等法院正式对顾颖琼发布了临时禁止令。在此前10月19日的洛杉矶听证会上，洛杉矶地区高等法院撤销了对顾颖琼的临时禁令，贾跃亭本人未出席。10月23日，贾跃亭在华盛顿州国王郡高等法院再次对顾颖琼申请临时禁制令并提起诽谤诉讼。（谭宵寒）</p><div id="left_hzh_ad">
                    <script async charset="utf-8" src="//d5.sina.com.cn/litong/zhitou/sinaads/release/sinaads.js"></script>
                    <script language="javascript" type="text/javascript" src="//d2.sina.com.cn/d1images/button/rotator.js"></script>
                    <script type="text/javascript">
                        (function(){
                            var adScript = document.createElement('script');
                            adScript.src = '//d1.sina.com.cn/litong/zhitou/sinaads/demo/wenjing8/js/yl_left_hzh_20171020.js';
                            document.getElementsByTagName('head')[0].appendChild(adScript);
                        })();
                    </script>

                </div></div></div></div>"""

selector = Selector(text=dd)

clearPaths = ['//script']
for path in clearPaths:
    blocks = selector.xpath(path).extract()
    for block in blocks:
        dd = dd.replace(block, '')
print dd