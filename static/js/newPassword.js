window.onload = function(){
    handleInputAndButton()
}

function handleInputAndButton(){
    let buttonSend = document.querySelector("#botaoNewPassword")
    buttonSend.disabled = true

    let newPassword = document.querySelector("#loginNewPasswordInput")
    let passwordConfirm = document.querySelector("#loginNewPasswordConfirmInput")
    let email = document.querySelector("#loginUserInput")

    passwordConfirm.addEventListener("keyup",()=>{
        buttonSend.disabled =  validateButton()
    })
    newPassword.addEventListener("keyup",()=>{
        buttonSend.disabled =  validateButton()
    })
    email.addEventListener("keyup",()=>{
        buttonSend.disabled =  validateButton()
    })
    buttonSend.setAttribute("onclick","sendData()")
}
function validateButton(){
    let email = document.querySelector("#loginUserInput").value
    let newPassword = document.querySelector("#loginNewPasswordInput").value
    let passwordConfirm = document.querySelector("#loginNewPasswordConfirmInput").value
    let diferentPassword = (newPassword != passwordConfirm) 
    let emptyInput = (!newPassword || !passwordConfirm || !email)
    return (diferentPassword || emptyInput)
}

async function sendData(){
    let url = forgetPasswordUrl
    body = formatBody()
    let buttonSend = document.querySelector("#botaoNewPassword").disabled
    if(!buttonSend){
        await fetch(url,{
            method:"POST",
            headers: {
                'Content-Type': 'application/json'
            },
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
    let user = document.querySelector("#loginUserInput").value
    let password = document.querySelector("#loginNewPasswordInput").value
    return JSON.stringify({
        "user":user,
        "password":password
    })
}
function cancel(){
    window.location.href="/login"
}