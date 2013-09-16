/*
* �����S���\��
* 
* 
*/

MY_DOMAIN = "127.0.0.1:5000";


function myPost(funcName, mydata, successFunc) {

	//�w�]��
	successFunc = successFunc || function(data){};
	mydata = mydata || "";
	
	$.ajax({
		type: "POST",
		async: false,
		contentType: "application/json",
		url: "http://" + MY_DOMAIN + "/" + funcName,
		data: JSON.stringify(mydata),
		success: function (data) {
			if (data == null) {
				alert("�L���");
			}
			else {
				successFunc(data);
			}
		},
		error: function (xhr, ajaxOptions, thrownError) {
			alert("�o�Ϳ��~ status:" + xhr.status + "," + xhr.responseText);
			alert("�o�Ϳ��~ :" + ajaxOptions + "," + thrownError);
		}
	});
}

function myGet(funcName, mydata, successFunc) {

	//�w�]��
	successFunc = successFunc || function(data){};
	
	$.ajax({
		type: "GET",
		async: false,
		contentType: "application/json",
		url: "http://" + MY_DOMAIN + "/" + funcName,
		data: JSON.stringify(mydata),
		success: function (data) {
			if (data == null) {
				alert("�L���");
			}
			else {
				successFunc(data);
			}
		},
		error: function (xhr, ajaxOptions, thrownError) {
			alert("�o�Ϳ��~ status:" + xhr.status + "," + xhr.responseText);
			alert("�o�Ϳ��~ :" + ajaxOptions + "," + thrownError);
		}
	});
}


//���o���}�C�Ƕi�Ӫ��Ѽ�
function getUrlVars() {
	var vars = [], hash;
	var hashes = window.location.search.slice(window.location.search.indexOf('?') + 1).split('&');
	for (var i = 0; i < hashes.length; i++) {
		hash = hashes[i].split('=');
		vars.push(hash[0]);
		vars[hash[0]] = hash[1];
	}
	//	console.log(vars);
	return vars;
}