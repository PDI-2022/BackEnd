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

//validacao de cadastro
const validFields = () => {
    return document.getElementById('form').reportValidity()
}

const saveUser = async () => {
    await auth()
    let url = "http://localhost:5000/api/v1/register"
    if(validFields()){
        const usuario = {
            user: document.getElementById('email').value,
            password: document.getElementById('senha').value
        }
        let response = await fetch(url,{
            method:"POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body:JSON.stringify(usuario)
        }).then(response=>{
            if(response.status != 201)
                window.alert("Ops, alguma coisa deu errado!")
            else{
                window.location.href = "/"
            }
        })
        let responseJson = await response.json()
        createUser(responseJson)
    }
}

//evento ao clicar em salvar
document.getElementById('salvar').addEventListener('click', saveUser)
document.getElementById('cancelar').addEventListener('click', ()=>{
    window.location.href = document.referrer
})