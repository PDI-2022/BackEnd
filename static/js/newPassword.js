window.onload = function(){
    handleInputAndButton()
}

function handleInputAndButton(){
    let buttonSend = document.querySelector("#botaoNewPassword")
    buttonSend.disabled = true
    let newPassword = document.querySelector("#loginNewPasswordInput")
    let passwordConfirm = document.querySelector("#loginNewPasswordConfirmInput")
    passwordConfirm.addEventListener("keyup",()=>{
        let buttonSend = document.querySelector("#botaoNewPassword")
        let newPassword1 = document.querySelector("#loginNewPasswordInput").value
        let passwordConfirm1 = document.querySelector("#loginNewPasswordConfirmInput").value
        if(!!newPassword1 && !!passwordConfirm1){
            buttonSend.disabled = (newPassword1 != passwordConfirm1)
        }
    })
    newPassword.addEventListener("keyup",()=>{
        let buttonSend = document.querySelector("#botaoNewPassword")
        let newPassword1 = document.querySelector("#loginNewPasswordInput").value
        let passwordConfirm1 = document.querySelector("#loginNewPasswordConfirmInput").value

        if(!!newPassword && !!passwordConfirm){
            buttonSend.disabled = (newPassword1 != passwordConfirm1)
        }
    })
    buttonSend.setAttribute("onclick","sendData")
}
async function sendData(){
    let url = "http://localhost:5000/api/v1/newPassword"
    body = formatBody()
    let buttonSend = document.querySelector("#botaoNewPassword").disabled
    if(!buttonSend){
        await fetch(url,{
            method:"POST",
            body:body
        }).then(response=>{
            if(response.status != 200)
                window.alert("Ops, alguma coisa deu errado!")
            else{
                window.location.href = "login"
            }
        })
    }
} 

function formatBody(){
    let user = document.querySelector("#loginUserInput")
    let password = document.querySelector("#loginNewPasswordInput")
    return JSON.stringify({
        "user":user,
        "password":password
    })
}