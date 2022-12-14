window.onload = async function () {
    await auth()
}

const localGet = () => JSON.parse(localStorage.getItem('dados_usuario')) ?? []

const localSet = async (dadosUsuario) => localStorage.setItem("dados_usuario", JSON.stringify(dadosUsuario))

const createUser = (usuario) => {
    const dadosUsuario = localGet()
    localSet(usuario)
}

const readUser = () => localGet()

const updateUser = (index, usuario) => {
    const dadosUsuario = readUser()
    dadosUsuario[index] = usuario
    localSet(dadosUsuario)
}

const deleteUser = (index) => {
    const dadosUsuario = readUser()
    dadosUsuario.splice[index, 1] = usuario
    localSet(dadosUsuario)
}

const validFields = () => {
    return document.getElementById('form').reportValidity()
}

const saveUser = async () => {
    await auth()
    let url = createUserUrl
    if(validFields()){
        const usuario = {
            user: document.getElementById('email').value,
            password: document.getElementById('senha').value
        }
        $('#modal-comp').modal({
            show:true,
            backdrop: 'static',
            keyboard: false
        })
        let response = await fetch(url,{
            method:"POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body:JSON.stringify(usuario)
        }).then(response=>{
            if(response.status != 201){
                $('#modal-comp').modal('hide');
                window.alert("Ops, alguma coisa deu errado!")
            }
            else{
                $('#modal-comp').modal('hide');
                $('#modal-redirecting').modal({
                    show:true,
                    backdrop: 'static',
                    keyboard: false
                })
                window.location.href = "/"
            }
        }).catch(err=>{
            $('#modal-comp').modal('hide');
            window.alert("Ops, alguma coisa deu errado!")
        })
        let responseJson = await response.json()
        createUser(responseJson)
    }
}

document.getElementById('salvar').addEventListener('click', saveUser)
document.getElementById('cancelar').addEventListener('click', ()=>{
    window.location.href = document.referrer
})