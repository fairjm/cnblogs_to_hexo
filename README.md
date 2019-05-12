# cnblogs_to_hexo
博客园文章(markdown)导出hexo  

实在受不了一些营销博客放广告刷评论,又又又搬家了...  
适用于使用`markdown`写作的博客园文章(也就是原本就需要是`markdown`格式的)  
进入`https://i.cnblogs.com/BlogBackup.aspx?type=1`进行备份,导出配置后即可.  

源代码里将`with open("CNBlogs_BlogBackup_1_201709_201905.xml", encoding="utf-8") as file:`改为自己的文件.  

默认会在当前目录产生`blog`和`images`两个文件.  
将`blog`内的md复制到hexo的`_posts`下,将`images`内的图片复制到`images`中即可.  

好久没写py了...写得丑请多多见谅 :)
