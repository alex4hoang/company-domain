<!DOCTYPE html>
<html>
<head>
	<title>Search Something</title>
	<meta name="ROBOTS" content="NOINDEX, NOFOLLOW" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0">

	<style type="text/css">
		* {
			font-family: Arial;
			font-size: 14px;
			line-height: 20px;
		}
		div {
			padding: 0 20px;
		}
		h1 {
			font-size: 18px;
		}
		.width-50 {
			max-width: 50%;
		}
		@media screen and (max-width: 720px) {
			p {
				max-width: 100% !important;
			}
			#searchdata {
				max-width: 280px;
			}
		}

		input {
			padding-bottom: 10px;
		}
		#search{
			padding:40px 0px;
		}
		#searchdata{
			margin: 0 0 10px 0;
			padding: 5px 15px;
			border:1px solid #0076a3;
			border-top-left-radius: 5px 5px;
			border-bottom-left-radius: 5px 5px;
		}
		.searchbutton {
			margin: 0;
			padding: 5px 15px;
			font-family: Arial, Helvetica, sans-serif;
			font-size:14px;
			outline: none;
			cursor: pointer;
			text-align: center;
			text-decoration: none;
			color: #ffffff;
			border: solid 1px #0076a3; border-right:0px;
			background: #0095cd;
			background: -webkit-gradient(linear, left top, left bottom, from(#00adee), to(#0078a5));
			background: -moz-linear-gradient(top,  #00adee,  #0078a5);
			border-top-right-radius: 5px 5px;
			border-bottom-right-radius: 5px 5px;
		}
		.searchbutton:hover {
			text-decoration: none;
			background: #007ead;
			background: -webkit-gradient(linear, left top, left bottom, from(#0095cc), to(#00678e));
			background: -moz-linear-gradient(top,  #0095cc,  #00678e);
		}
		/* Fixes submit button height problem in Firefox */
		.searchbutton::-moz-focus-inner {
		  border: 0;
		}
		.clear{
			clear:both;
		}
		.no-mobile {
			color: #aaa;
			margin-top: -20px;
		}
	</style>
</head>

<body>
	<div>
		<form id="search" onsubmit="gotopage();return false;">
				<input id="searchdata" type="text" size="38" maxlength="200" placeholder="{{text}}"><input type="reset" value="Get" class="searchbutton">
		</form>
		<p class="no-mobile">Not yet mobile compatible.</p>
	<div class="clear"></div>
	</div>
</body>

<script>
	function gotopage() {
		var new_url = '';
		var name = document.getElementById('searchdata').value;
		url = window.location.href;
		if (url.substr(-1) == '/') {
			new_url = url + name;
		}
		else {
			new_url = url + "/" + name;
		}
		window.location.assign(new_url);
		return false;
	}
</script>

</html>

