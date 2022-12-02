function displayApplication(){
    applicationBody = document.querySelector("body")
    applicationBody.removeAttribute("class")
    sessionStorage.setItem("displayWelcomeScreen","false")
    let animation = document.querySelector("#animation")
    let main = document.querySelector("body")
    main.removeChild(animation)
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