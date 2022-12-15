function displayApplication(){
    applicationBody = document.querySelector("body")
    applicationBody.removeAttribute("class")
    sessionStorage.setItem("displayWelcomeScreen","false")
    let animation = document.querySelector("#animation")
    let body = document.querySelector("body")
    body.removeChild(animation)
    let main = document.querySelector("main")
    main.style.display = "block"
}

function animationLoadFunction(applicationBody){
    let displayWelcomeScreen = sessionStorage.getItem("displayWelcomeScreen")

    if(displayWelcomeScreen == "false"){
        displayApplication()
    }
    else{
        applicationBody = document.querySelector("body")
        applicationBody.setAttribute("class","disableOverflow")
    }
    return applicationBody
}