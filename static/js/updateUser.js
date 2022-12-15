let infos
window.onload = function(){
    infos = JSON.parse(localStorage.getItem("userToUpdate"))
    if(!!infos){
        const email = document.querySelector("#email")
        email.value = infos.email
    }
    let cancelButton = document.querySelector("#cancelar")
    cancelButton.addEventListener("click", ()=> window.location.href = "/userList")
    let updateButton = document.querySelector("#update")
    updateButton.addEventListener("click", updateUser)
}
async function updateUser(){
    $('#modal-comp').modal({
        show:true,
        backdrop: 'static',
        keyboard: false
    });  
    let data = {
        user:document.querySelector("#email").value,
        password:document.querySelector("#senha").value,
    }
    let url = `http://localhost:5000/api/v1/users/${infos.id}`
    await fetch(url,{
        method:"PATCH",
        headers:{
            'Content-type':'application/json'
        },
        body:JSON.stringify(data)
    }).then(resp=>{
        $('#modal-comp').modal('hide');  
        if(resp.status != 200){
            window.alert("Ocorreu um erro com a atualização do usuário")
        }
        else{
            $('#modal-redirecting').modal({
                show:true,
                backdrop: 'static',
                keyboard: false
            });  
            window.location.href = "/userList"
            $('#modal-redirecting').modal('hide')
        }
    }).catch(err=>{
        window.alert("Ocorreu um erro com a atualização do usuário")
        $('#modal-comp').modal('hide');  
    })
    $('#modal-comp').modal('hide');  
}