sd打标自用小工具,由gpt完成,处理同图片的相同txt,批量or单个，添加 移除，前置，替换,通过txt校验图片的相似度。有什么需求丢给gpt让它改就行。<br>
1.相似度检测，指定一个值，对比每个txt之间的差异计算图片相似度,相似则移动到一个文件夹<br>
2.检测tag并移动,检测每个txt的tag，包含则把图片和txt移动到deleted_files文件夹<br>
3.替换tag,添加tag,移除tag,字面意思<br>
4.to_png_remove 把当前文件夹图片全部格式转为png，用哈希检测有没有重复的，重复就删了，最后再过一遍图片完整性检测<br>
5.yande.tag，看文件里面很简单。<br>
6.顺序重命名所有图片<br>
