var formData = new FormData()

const validFormats = [
    ".zip",
    ".tar",
    ".7zip",
]

window.onload = async function () {
    await auth()
    handleSendButton()
}

function stateHandle(button,input) {
    let field
    if(input == "name")
        field = document.querySelector("#InputName").value
    else if(input == "description")
        field = document.querySelector("#InputDescription").value
    formData.delete(input)
    formData.append(input,field)
    let validator = !!formData.get("name") && !!formData.get("model") && !!formData.get("description")

    button.disabled = !validator
}

function handleSendButton(){
    let button = document.querySelector("#sendModelBtn");
    let nameInput = document.querySelector("#InputName");
    let description = document.querySelector("#InputDescription");

    button.disabled = true;
    nameInput.addEventListener("keyup",()=>{
        stateHandle(button,"name")
    }); 
    description.addEventListener("keyup",()=>{
        stateHandle(button,"description")
    }); 
}

function dropHandler(event) {
    try {
        event.preventDefault();
        const item = event.dataTransfer.items

        if (item.length > 0) {
            const itemAsFile = item[0].getAsFile()
            validateFile(itemAsFile,itemAsFile.name)
        }
        else {
            throw new Error("Arquivo com problema")
        }
    }
    catch (err) {
        console.error(err)
    }
}

function dragOverHandler(event) {
    event.preventDefault();
}

function uploadFileInput(event) {
    if (event.target.files.length > 0) {
        validateFile(event.target.files[0],event.target.files[0].name)
    }
}

function validateFile(itemAsFile,name) {
    formData.delete("model")
    const format = name.substring(name.lastIndexOf("."))
    if (validateFormat(format)) {
        formData.append("model",itemAsFile)
        let fileContainer = document.querySelector('#file-label')
        !fileContainer ? showTextAndIcon(name) : updateTextAndIcon(name)
        let button = document.querySelector("#sendModelBtn");
        stateHandle(button)
    }
    else {
        window.alert("Ocorreu um erro com o upload o modelo:\nFormato inv??lido " + `${format}`)
    }
}

function validateFormat(name){
    return validFormats.includes(name)
}

async function sendModel(){
    await auth()
    let button = document.querySelector("#sendModelBtn");
    button.disabled = true
    $('#modal-comp').modal({
        show:true,
        backdrop: 'static',
        keyboard: false
    });  
    let url = createModelUrl
    await fetch(url,{
          method: 'POST',
          body: formData
    }).then(response=>{
        $('#modal-comp').modal('hide');
        if(response.status == 201){
            $('#modal-redirecting').modal({
                show:true,
                backdrop: 'static',
                keyboard: false
            })
            window.location.href = "/"
        }
        else{
            window.alert("Ocorreu um erro")
        }
    }).catch(err=>{
        button.disabled = false
        $('#modal-comp').modal('hide');
        $('#modal-erro').modal({
            show:true,
            backdrop: 'static',
            keyboard: false
        })
        console.error(err)
    }).finally(_=>{
        $('#modal-comp').modal('hide');
    })
}
function showTextAndIcon(name) {
    var elem1 = document.createElement('img')
    var elem2 = document.createElement('label');
    elem2.setAttribute('id', `file-label`);
    elem2.innerHTML = name;
    elem1.classList.add("icon-upload");
    elem2.classList.add("label-icon-upload");
    document.getElementsByClassName('fileContainer')[0].appendChild(elem1);
    document.getElementsByClassName('fileContainer')[0].appendChild(elem2);

}

function updateTextAndIcon(name) {
    let id = `file-label`;
    let imgLabel = document.querySelector("#" + id);
    imgLabel.innerHTML = name;
}

