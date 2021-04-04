function edit_prompt(id){
    modal.style.display = "block";
    console.log(id);
    console.log("i am in edit prompt");
    document.getElementById("modal_id").value= id;
//    $.post('/edit',{"id": id,}, function(response, status){
//        console.log(id,"Posted to backend for edit");
//    });
}

function delete_prompt(id){
    console.log(id);
    console.log("i am in delete prompt");
    $.post('/delete',{"id": id}, function(response, status){
        console.log(id,"Posted to backend for delete");
        alert("Entry Deleted!")
        window.location.href = '';
    });
}

function download_attachment(primary_key){
    console.log("attach_primaery_key",primary_key);
     $.post('/download',{"primary_key": primary_key}, function(response, status){
        console.log(primary_key,"Asked backend for download",response,status);
        console.log(typeof response,"typpppee");
         window.location.href = response;


    });
}

function top_nav_bar() {
  var x = document.getElementById("myTopnav");
  if (x.className === "topnav") {
    x.className += " responsive";
  } else {
    x.className = "topnav";
  }
}

//file upload button
var W3CDOM = (document.createElement && document.getElementsByTagName);

function initFileUploads() {
	if (!W3CDOM) return;
	var fakeFileUpload = document.createElement('div');
	fakeFileUpload.className = 'fakefile';
	fakeFileUpload.appendChild(document.createElement('input'));
	var image = document.createElement('img');
	image.src='pix/button_select.gif';
	fakeFileUpload.appendChild(image);
	var x = document.getElementsByTagName('input');
	for (var i=0;i<x.length;i++) {
		if (x[i].type != 'file') continue;
		if (x[i].parentNode.className != 'fileinputs') continue;
		x[i].className = 'file hidden';
		var clone = fakeFileUpload.cloneNode(true);
		x[i].parentNode.appendChild(clone);
		x[i].relatedElement = clone.getElementsByTagName('input')[0];
		x[i].onchange = x[i].onmouseout = function () {
			this.relatedElement.value = this.value;
		}
	}
}

function user_added(){
   
    alert("User added !");
}