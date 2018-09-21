# -*- coding:utf-8 -*-

# 1.美女吧内选取所有帖子的a标签内的href属性值，即每个帖子的链接地址
# 会员
# <div class='threadlist_title pull_left j_th_tit  member_thread_title_frs'></div>
# 会员父级的父级
# <div class='threadlist_lz clearfix'></div>
#
# 非会员
# <div class='threadlist_title pull_left j_th_tit'></div>
# 非会员父级的父级
# <div class='threadlist_lz clearfix'></div>

# XPath的表达式
# //div[@class="threadlist_lz clearfix"]//a[@class="j_th_tit"]/@href
# 选取所有的a标签的href属性值
# https://tieba.baidu.com
# https://tieba.baidu.com/p/5779124772
# https://tieba.baidu.com/p/5772994595
# https://tieba.baidu.com/p/5771500721
# https://tieba.baidu.com/p/5770168580
# https://tieba.baidu.com/p/5769421593
# https://tieba.baidu.com/p/5766661549
# https://tieba.baidu.com/p/5764044600
# https://tieba.baidu.com/p/5764043755
# https://tieba.baidu.com/p/5763002801
# https://tieba.baidu.com/p/5762961058
# https://tieba.baidu.com/p/5761185787
# https://tieba.baidu.com/p/5759959887
# https://tieba.baidu.com/p/5759690470
# https://tieba.baidu.com/p/5758365604
# https://tieba.baidu.com/p/5757963352
# https://tieba.baidu.com/p/5755226460
# https://tieba.baidu.com/p/5755285875
# https://tieba.baidu.com/p/5754995810
# https://tieba.baidu.com/p/5753419436
# https://tieba.baidu.com/p/5748319958
# https://tieba.baidu.com/p/5748017204
# https://tieba.baidu.com/p/5746783450
# https://tieba.baidu.com/p/5746226093
# https://tieba.baidu.com/p/5745324235
# https://tieba.baidu.com/p/5745316093
# https://tieba.baidu.com/p/5743731643
# https://tieba.baidu.com/p/5743630942
# https://tieba.baidu.com/p/5743726136
# https://tieba.baidu.com/p/5742064303
# https://tieba.baidu.com/p/5742058912
# https://tieba.baidu.com/p/5742050405
# https://tieba.baidu.com/p/5737446489
# https://tieba.baidu.com/p/5737440833
# https://tieba.baidu.com/p/5737266452
# https://tieba.baidu.com/p/5735872022
# https://tieba.baidu.com/p/5734417117
# https://tieba.baidu.com/p/5734403112
# https://tieba.baidu.com/p/5732806350
# https://tieba.baidu.com/p/5732811320
# https://tieba.baidu.com/p/5732819428
# https://tieba.baidu.com/p/5731413307
# https://tieba.baidu.com/p/5725593253
# https://tieba.baidu.com/p/3990313783
# https://tieba.baidu.com/p/5585349374
# https://tieba.baidu.com/p/5551307878
# https://tieba.baidu.com/p/5529120289
# https://tieba.baidu.com/p/5483519002
# https://tieba.baidu.com/p/5462958825
# https://tieba.baidu.com/p/5434086744

# 2.贴吧内每个帖子图片的连接地址，此连接地址可打开图片
# XPath的匹配规则
# //cc//img[@class="BDE_Image"]/@src
# 取出的图片连接地址
# https://imgsa.baidu.com/forum/w%3D580/sign=31d1d7ab59fbb2fb342b581a7f4b2043/29adcbef76094b36c490c41bafcc7cd98c109dc2.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=576356f7506034a829e2b889fb1249d9/49da81cb39dbb6fd9c203ad00524ab18962b37c9.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=bba253d4c4fcc3ceb4c0c93ba244d6b7/6b8da9773912b31b4ce312df8a18367adbb4e1be.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=807bc5e8b5389b5038ffe05ab534e5f1/23c79f3df8dcd1000c0b27d77e8b4710b8122fb5.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=a089de5d0f3b5bb5bed720f606d2d523/ac8f8c5494eef01fb294c733ecfe9925bd317d40.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=daace43217d5ad6eaaf964e2b1ca39a3/ab1c8701a18b87d62fc874e90b0828381e30fdba.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=37f4cc5155ee3d6d22c687c373146d41/c8a20cf431adcbef10c0a1f0a0af2edda2cc9f54.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=0bc3912a58e736d158138c00ab524ffc/7f09c93d70cf3bc72cf0121add00baa1cc112a50.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=66ce4dd8a4d3fd1f3609a232004f25ce/9a025aafa40f4bfb1fa840a20f4f78f0f63618c8.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=1826a2920523dd542173a760e108b3df/1124ab18972bd407e6cf0d0b77899e510fb30938.jpg
# https://imgsa.baidu.com/forum/w%3D580/sign=40dbb228316d55fbc5c6762e5d234f40/14f431adcbef76092d7a476922dda3cc7dd99ed7.jpg

