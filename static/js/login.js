var applicationBody

window.onload = function(){
    let main = document.querySelector("main")
    main.style.display = "none"
    applicationBody = animationLoadFunction(applicationBody)
    document.cookie= "token="
}

async function login(){
    let body = formatBody()
    let url = loginUrl
    let response = await fetch(url,{
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body:body
    }).catch(err=>{
        console.error(err)
        window.alert("Usuário e/ou senha inválidos")
    })
    if(response.status != 200)
        window.alert("Usuário e/ou senha inválidos")
    else{
        let json = await response.json()
        if(!!json){
            sessionStorage.setItem("token",json.token)
            document.cookie = "token="+json.token
            window.location.href = "/"
        }
        else{
            window.alert("Usuário e/ou senha inválidos")
        }
    }

}

function formatBody(){
    let user = document.querySelector("#loginUserInput").value
    let password = document.querySelector("#loginPasswordInput").value
    return JSON.stringify({
        "user":user,
        "password":password
    })
}