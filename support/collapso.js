/*---------------------------- Expander variables ---------------------------*/

var linkedList = new Array();
var divTextFull = new Array();
var divTextShort = new Array();

var classIndependent = 'expanderIndependent';
var classLinked = 'expanderLinked';
var classHeading = 'expanderHeading';
var classContent = 'expanderContent';
var classMore = 'expanderMore';

var divPadding = 10;

var altExpand = 'Expand';
var altCollapse = 'Collapse';
var srcExpand = 'doc/plus.gif';
var srcCollapse = 'doc/minus.gif';

var textMore = 'more...';
var textLess = '...less';
var textMoreClass = 'linkMore';
var textLessClass = 'linkLess';
var moreCutoff = 12;

/*---------------------------- Slider variables ---------------------------*/

var timerlen = 3;
var slideAniLen = 300;
var timerID = new Array();
var startTime = new Array();
var obj = new Array();
var endHeight = new Array();
var moving = new Array();
var dir = new Array();

/*---------------------------- Expander functions ---------------------------*/

function initialiseDivs() {

	var divs = document.getElementsByTagName('DIV');
	var divCount = 1;
	var moreCount = 1;
	var linkedCount = 0;
	var openType = 'Independent';
	var divContent = '';
	var contentWords = new Array();
	
	for(var i=0;i<divs.length;i++) {

    // Process expanderMore Divs
		if (divs[i].className == classMore) {
		
			divs[i].id = 'expander_more_' + moreCount;
		  divTextFull[moreCount] = document.getElementById(divs[i].id).innerHTML;
      contentWords[moreCount] = divTextFull[moreCount].split(" ");
      divTextShort[moreCount] = '';
      
      for (wordCount = 0; wordCount < moreCutoff; wordCount++) { divTextShort[moreCount] = divTextShort[moreCount] + contentWords[moreCount][wordCount] + " "; }
      
      divTextShort[moreCount] = divTextShort[moreCount] + '<span class="' + textMoreClass + '" onclick="toggleMore(\'expander_more_' + moreCount + '\')">' + textMore + '</span></p>';
      divTextFull[moreCount] = divTextFull[moreCount] + '<p class="' + textLessClass + '" onclick="toggleMore(\'expander_more_' + moreCount + '\')">' + textLess + '</p>';
      document.getElementById(divs[i].id).innerHTML = divTextShort[moreCount];
      
      moreCount++;
    
    }    

  }

	for(var i=0;i<divs.length;i++) {

		if (divs[i].className == classIndependent) { openType = 'Independent'; }

		if (divs[i].className == classLinked) {
			openType = 'Linked';
			linkedCount++;
			linkedList[linkedCount] = '|';
		}
		
    if (divs[i].className == classHeading) {
    
			divs[i].innerHTML = '<a id="expander_link_' + divCount + '">' + divs[i].innerHTML + '<img id="expander_control_' +  divCount + '" src="' +  srcExpand  + '" alt="' +  altExpand  + '" /></a>';

			if (openType == 'Independent') {
			  //document.getElementById('expander_control_' +  divCount).onclick = toggleIndependent;
			  document.getElementById('expander_link_' +  divCount).onclick = toggleIndependent;
			}
			
			if (openType == 'Linked') {
				//document.getElementById('expander_control_' +  divCount).onclick = toggleLinked;
				document.getElementById('expander_link_' +  divCount).onclick = toggleLinked;
				linkedList[linkedCount] = linkedList[linkedCount] + 'expander_content_' + divCount + '|';
			}
			
			divs[i].id = 'expander_heading_' + divCount;
			divs[i+1].id = 'expander_content_' + divCount;
			divContent = document.getElementById(divs[i+1].id).innerHTML;
			
			document.getElementById('expander_content_' + divCount).style.height = (document.getElementById('expander_content_' + divCount).scrollHeight - divPadding) + 'px';
			document.getElementById('expander_content_' + divCount).style.display = 'none';
			document.getElementById('expander_content_' + divCount).style.overflow = 'hidden';
			
			divCount++;
		}    
	}
	
}

function toggleIndependent() {

	contentID = this.id.replace('link', 'content');
	imageID = this.id.replace('link', 'control');
	imageElement = document.getElementById(imageID);

	if (document.getElementById(contentID).style.display == 'block') {
		imageElement.alt = altExpand;
		imageElement.src = srcExpand;
		slideup(contentID);
	}	else {
		imageElement.alt = altCollapse;
		imageElement.src = srcCollapse;
		slidedown(contentID);
	}
}

function toggleLinked() {

	contentID = this.id.replace('link', 'content');
	imageID = this.id.replace('link', 'control');
	imageElement = document.getElementById(imageID);

	if (document.getElementById(contentID).style.display == 'block') {
		imageElement.alt = altExpand;
		imageElement.src = srcExpand;
		slideup(contentID);
	} else {
		for (var i = 1; i < linkedList.length; i++) {
			if (linkedList[i].indexOf(contentID) > 0) {
				linkedDivs = linkedList[i].split('|')
				for(var j = 1; j < linkedDivs.length-1; j++) {
					slideup(linkedDivs[j]);
					document.getElementById(linkedDivs[j].replace('content', 'control')).src = srcExpand;
					document.getElementById(linkedDivs[j].replace('content', 'control')).alt = altExpand;
				}
			}
		}
		imageElement.alt = altCollapse;
		imageElement.src = srcCollapse;
		slidedown(contentID);
	}
}

function toggleMore(contentID) {

	var idParts = new Array();
	idParts = contentID.split('_');
	contentCount = idParts[idParts.length-1];

	if (document.getElementById(contentID).innerHTML.indexOf(textLessClass) >= 0) {
		document.getElementById(contentID).innerHTML = divTextShort[contentCount];
		e = document.getElementById(contentID);
		while (e.tagName != 'BODY') {
		  if (e.className.indexOf(classContent) > -1) {
		    e.style.overflow = 'visible';
		    e.style.height = 'auto';
		  }
		  e = e.parentNode;
		}
	}	else {
		document.getElementById(contentID).innerHTML = divTextFull[contentCount]
		e = document.getElementById(contentID);
		while (e.tagName != 'BODY') {
		  if (e.className.indexOf(classContent) > -1) {
		    e.style.overflow = 'visible';
		    e.style.height = 'auto';
		  }
      e = e.parentNode;
		}
	}
}


/*---------------------------- Slider functions ---------------------------*/

function slidedown(objname) {

  document.getElementById(objname).style.overflow = 'hidden';
  document.getElementById(objname).style.height = (document.getElementById(objname).scrollHeight - divPadding) + 'px';
  
	if (moving[objname]) { return; }
	if (document.getElementById(objname).style.display != "none") {	return; } // cannot slide down something that is already visible

	moving[objname] = true;
	dir[objname] = "down";
	startslide(objname);
}

function slideup(objname) {

  document.getElementById(objname).style.overflow = 'hidden';
  document.getElementById(objname).style.height = (document.getElementById(objname).scrollHeight - divPadding) + 'px';

	if (moving[objname]) { return; }
	if (document.getElementById(objname).style.display == "none") { return; } // cannot slide up something that is already hidden

	moving[objname] = true;
	dir[objname] = "up";
	startslide(objname);
}

function startslide(objname){

	obj[objname] = document.getElementById(objname);
	endHeight[objname] = parseInt(obj[objname].style.height);
	startTime[objname] = (new Date()).getTime();

	if(dir[objname] == "down") { obj[objname].style.height = "1px"; }

	obj[objname].style.display = "block";
	timerID[objname] = setInterval('slidetick(\'' + objname + '\');', timerlen);
}

function slidetick(objname) {

	var elapsed = (new Date()).getTime() - startTime[objname];

	if (elapsed > slideAniLen) {
	  endSlide(objname);
	} else {
		var d = Math.round(elapsed / slideAniLen * endHeight[objname]);
		if (dir[objname] == "up") { d = endHeight[objname] - d; }
		obj[objname].style.height = d + "px";
	}

	return;
}

function endSlide(objname) {

	clearInterval(timerID[objname]);

	if (dir[objname] == "up") { obj[objname].style.display = "none"; }

	// obj[objname].style.height = obj[objname].scrollheight;
  obj[objname].style.height = endHeight[objname] + "px";

	delete(moving[objname]);
	delete(timerID[objname]);
	delete(startTime[objname]);
	delete(endHeight[objname]);
	delete(obj[objname]);
	delete(dir[objname]);

	return;
}