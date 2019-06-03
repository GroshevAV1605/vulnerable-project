function handleTabChange(evt, tabName) {
    /*isAuthTab = isauth;
        let tablinks = document.getElementsByClassName("tablink");
        for (let i = 0; i < tablinks.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        this.currentTarget.className += " active";*/

    let i, tabcontent, tablink;
    tabcontent = document.getElementsByClassName("tab-content");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    tablinks = document.getElementsByClassName("tablink");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    document.getElementById(tabName).style.display = "flex";
    evt.currentTarget.className += " active";
}

function searchItem(){
    var searchSTR = document.getElementById("searchPost").value;
    var dat = {'data':searchSTR};
}