var listColors=["#800080","#FF00FF","#000080","#0000FF","#008080","#00FFFF","#008000","#00FF00","#808000","#FFFF00","#800000","#FF0000","#000000","#808080"];


return (function draw(left, top, width, height) {
for(var i = 0; i<left.length; i++)
{
color=i%listColors.length
document.body.innerHTML += "<div id='border' style='border-style:solid;position:absolute;color:"+listColors[i]+";left:"+left[i]+"px;top:"+top[i]+"px;height:"+height[i]+"px;width:"+width[i]+"px;'></div>"
}

})(arguments[0], arguments[1], arguments[2], arguments[3]);