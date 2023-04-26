function openPage(){
    var x = document.getElementById("search").value;

    if(x === 'store'){
        window.open("/store")
    }

    if(x === 'home'){
        window.open('/home')
    }

    if(x === 'group'){
        window.open("/group")
    }

    if(x === 'schedule'){
        window.open("/schedule")
    }
}