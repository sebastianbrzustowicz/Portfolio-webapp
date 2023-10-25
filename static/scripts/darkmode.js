
function darkmode(){
    var profilewrapper_exist = document.getElementById("profile-wrapper");
    var profilecards = []
    for (var i = 0; i <= 30; i++)
        if (document.getElementById("profile-card"+i) !== null) profilecards[i] = 1;
        else profilecards[i] = 0;
    if (document.getElementById("checkboxID").checked == false){ //dark mode
        document.getElementById("body").style.setProperty('background-color', 'black', 'important');
        if (profilewrapper_exist){
            document.getElementById("profile-wrapper").classList.remove("divcard");
            document.getElementById("profile-wrapper").classList.add("divcard_animated");
            document.getElementById("profile-wrapper").style.setProperty('background-color', '#404040', 'important');
            document.getElementById("profile-wrapper").style.setProperty('color', 'white', 'important');}
        for (var i = 0; i <= 30; i++){
        if (profilecards[i]){
            document.getElementById("profile-card"+i).classList.remove("divcard");
            document.getElementById("profile-card"+i).classList.add("divcard_animated");
            document.getElementById("profile-card"+i).style.setProperty('background-color', '#404040', 'important');
            document.getElementById("profile-card"+i).style.setProperty('color', 'white', 'important');}
        }
    }else{ //white mode
        document.getElementById("body").style.setProperty('background-color', '#D6ECF3', 'important');
        if (profilewrapper_exist){
            document.getElementById("profile-wrapper").classList.remove("divcard");
            document.getElementById("profile-wrapper").classList.add("divcard_animated");
            document.getElementById("profile-wrapper").style.setProperty('background-color', 'white', 'important');
            document.getElementById("profile-wrapper").style.setProperty('color', 'black', 'important');}
        for (var i = 0; i <= 30; i++){
        if (profilecards[i]){
            document.getElementById("profile-card"+i).classList.remove("divcard");
            document.getElementById("profile-card"+i).classList.add("divcard_animated");
            document.getElementById("profile-card"+i).style.setProperty('background-color', 'white', 'important');
            document.getElementById("profile-card"+i).style.setProperty('color', 'black', 'important');
        }
    }
    }
}

function save(){
    
    var checkbox = document.getElementById("checkboxID");//
    console.log(document.getElementById("checkboxID").checked);
    if (document.getElementById("checkboxID").checked==true){
    localStorage.setItem("checkboxStorage", true);//
    console.log("Storage saved from checkbox to: true");
    }
    else{
    localStorage.setItem("checkboxStorage", false);//
    console.log("Storage saved from checkbox to: false");
    }

    darkmode();
    
}

document.querySelector('.switch div').style.removeProperty('-webkit-transition');
document.querySelector('.switch div').style.removeProperty('-moz-transition');
document.querySelector('.switch div').style.removeProperty('transition');
document.querySelector('body').style.removeProperty('transition');

console.log(localStorage.getItem("checkboxStorage"));

if (localStorage.getItem("checkboxStorage")==null) save();

var checkbox = document.getElementById("checkboxID");

if (localStorage.getItem("checkboxStorage").valueOf()==="true".valueOf()){
    document.getElementById("checkboxID").checked = true;
    darkmode();
    console.log("Loaded from DB: true");
}
else if (localStorage.getItem("checkboxStorage").valueOf()==="false".valueOf()){
    document.getElementById("checkboxID").checked = false;
    darkmode();
    console.log("Loaded from DB: false");
}
else if (document.getElementById("checkboxID").checked==true){
    localStorage.setItem("checkboxStorage", checkbox.true);
    darkmode();
    console.log("Loaded from checkbox: true");
}
else if (document.getElementById("checkboxID").checked==false){
    localStorage.setItem("checkboxStorage", checkbox.false);
    darkmode();
    console.log("Loaded from checkbox: false");
}

function animation_start(){
document.querySelector('.switch div').style.setProperty('-webkit-transition', 'all 300ms');
document.querySelector('.switch div').style.setProperty('-moz-transition', 'all 300ms');
document.querySelector('.switch div').style.setProperty('transition', 'all 300ms');
document.querySelector('body').style.setProperty('transition', '1s ease');
var profilecards = []
    for (var i = 0; i <= 30; i++)
        if (document.getElementById("profile-card"+i) !== null) document.getElementById("profile-card"+i).style.setProperty('transition', '0.7s ease');

}

save();

document.getElementById("checkboxID").addEventListener('change', save);

function delete_animation(){
    document.getElementById("profile-wrapper").classList.remove("divcard_animated");
    document.getElementById("profile-wrapper").classList.add("divcard");
    document.getElementById("profile-card0").classList.remove("divcard_animated");
    document.getElementById("profile-card1").classList.remove("divcard_animated");
    document.getElementById("profile-card2").classList.remove("divcard_animated");
}

//window.addEventListener('change', save);