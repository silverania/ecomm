function getPosition() {

      docBodyScrollHeight=document.body.scrollHeight;
      docDocElementScrollHeight=document.documentElement.scrollHeight;
      docBodyOffsetHeight=document.body.offsetHeight;
      docDocElementOffsetHeight=  document.documentElement.offsetHeight;
      docBodyClientHeight=document.body.clientHeight;
      docDocElementClientHeight=document.documentElement.clientHeight;
      let totalHeight = Math.max(
      document.body.scrollHeight, document.documentElement.scrollHeight,
      document.body.offsetHeight, document.documentElement.offsetHeight,
      document.body.clientHeight, document.documentElement.clientHeight
    );
     val=docDocElementOffsetHeight-docDocElementClientHeight;
  let tagElmnt = document.getElementById("page");
  var actualHeight = document.documentElement.scrollTop;
  /*alert(actualHeight+"val_"+docBodyScrollHeight+"_"+docDocElementOffsetHeight+"_docbodyoffsetheight"+docBodyOffsetHeight
  +"docDocElementOffsetHeight"+docDocElementOffsetHeight+"docBodyClientHeight"+docBodyClientHeight+"docDocElementClientHeight"+docDocElementClientHeight);*/
  let rapport=parseInt((actualHeight/val)*100);

  createProgressBar(rapport);
}

function createProgressBar(actualValue){
  var object=document.getElementById('progressbar');
  object.value=parseInt(actualValue,10);
}
