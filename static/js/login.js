var applicationBody

window.onload = function(){
    applicationBody = animationLoadFunction(applicationBody)
}

async function login(){
    let body = formatBody()
    let url = "http://localhost:5000/api/v1/login"
    let response = await fetch(url,{
        method: "POST",
        body:body
    }).then(response=>{
        if(response.status != 200)
            window.alert("Usuário e/ou senha inválidos")
    }).catch(err=>{
        console.error(err)
        window.alert("Usuário e/ou senha inválidos")
    })
    let json = await response.json()
    if(!!json){
        sessionStorage.setItem("token",json)
    }
    else{
        window.alert("Usuário e/ou senha inválidos")
    }
}

function formatBody(){
    let user = document.querySelector("#loginUserInput")
    let password = document.querySelector("#loginPasswordInput")
    return JSON.stringify({
        "user":user,
        "password":password
    })
}

async function auth(){
    let url = "http://localhost:5000/api/v1/authenticate"
    let token = sessionStorage.getItem("token")
    let response = await fetch(url,{
        method: "POST",
        body:token
    }).then(response=>{
        if(response.status == 401)
            window.location.href = "login"
    }).catch(err=>{
        window.location.href = "login"
    })
    let json = await response.json()
    if(json == "autorizado")
        return
    else
        window.location.href = "login"
}