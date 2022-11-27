let body = {
    main:"",
    footer:"", 
    header:""
}
var applicationBody

function getPageBody(){
    body.main = document.querySelector("main")
    body.footer = document.querySelector("footer")
    body.header = document.querySelector("header")
}

function displayApplication(){
    applicationBody = document.querySelector("body")
    applicationBody.removeAttribute("class")
    sessionStorage.setItem("displayWelcomeScreen","false")
    let animation = document.querySelector("#animation")
    let main = document.querySelector("body")
    main.removeChild(animation)
}

window.onload = function () {

    let modelHolder = document.querySelector(".modelHolder")
    getPageBody()
    let displayWelcomeScreen = sessionStorage.getItem("displayWelcomeScreen")

    if(displayWelcomeScreen == "false"){
        displayApplication()
    }
    else{
        applicationBody = document.querySelector("body")
        applicationBody.setAttribute("class","disableOverflow")
    }
    
    let inputClass = document.querySelector("#InputClass")

    localStorage.clear();
    modelHolder.style.display = "none"
    
    inputClass.addEventListener("change",()=>{
        let modelHolder = document.querySelector(".modelHolder")
        modelHolder.style.display = inputClass.checked ? "flex" : "none" 
    })
}

function returnHome(){
    window.location.href = '/'
}
function dragOverHandler(event, input) {
    event.preventDefault();
}

async function sendToBack() {
    let displayClassificationInfos = document.querySelector("#InputClass").checked
    let generatePageWithImages = document.querySelector("#InputPagaWithImages").checked
    let modelId = displayClassificationInfos ? document.querySelector("select").value : -1
    var tableAux = 0

    if(!!json["interna"] && !!json["externa"]){
        var req = new XMLHttpRequest();
        req.timeout = 10 * 60 * 1000;
        const url = new String("http://127.0.0.1:5000/api/v1/process");
        req.open('POST',url,true);
        req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");

        data = {
            "displayClassificationInfos":displayClassificationInfos,
            "modelId":modelId,
            "generatePageWithImages":generatePageWithImages,
            "internalImg":json["interna"],
            "externalImg":json["externa"]
        }

        req.addEventListener("readystatechange", function () {
            if (this.readyState === 4 && req.status != 200) {
                $('#modal-comp').modal('hide'); 
                $('#modal-erro').modal({
                    show:true,
                    backdrop: 'static',
                    keyboard: false
                })
            }
            else if(this.readyState === 4 && req.status == 200){
                localStorage.setItem("csv",req.response)
                $('#modal-comp').modal('hide'); 

                var showIconAndName = false
                if (!localStorage.getItem('csv')) {
                    showIconAndName = true;
                }
                if(localStorage.getItem('csv') != '' && tableAux == 0){
                    $('#modal-comp').modal('hide');

                    if(generatePageWithImages){
                        window.location.href = "/seeds"
                        $('#modal-redirecting').modal({
                            show:true,
                            backdrop: 'static',
                            keyboard: false
                        })
                    }
                    else{
                        generateDownloadScreen()
                    }
                    tableAux = 1
                }
                if (showIconAndName == true) {
                    showIconAndName = false;
                }
            }
        });
        req.send(JSON.stringify(data))
        new Promise(() => {
            $('#modal-comp').modal({
                show:true,
                backdrop: 'static',
                keyboard: false
            });                
        }, rej=>{
            console.error(rej)
        });
    }
}

function generateDownloadScreen(){
    let selectBody = document.querySelector("body")
    selectBody.setAttribute("class","downloadScreen")
    selectBody.removeChild(body.main)
    selectBody.removeChild(body.footer)
    if(!document.getElementsByTagName("download-section")[0]){
        let download = document.createElement("download-page");
        selectBody.appendChild(download)
    }
    selectBody.appendChild(body.footer)
}

function downloadCsv() {
    const csvString = localStorage.getItem('csv');
    var blob = new Blob([csvString], { type: 'text/plain;charset=utf-8;' });
    var link = document.createElement("a");
    if (link.download !== undefined) {
        var url = URL.createObjectURL(blob);
        link.setAttribute("href", url);
        link.setAttribute("download", "Arquivo.csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        window.location.href ="/"
    }
}

let buttons = document.querySelectorAll(".botaoEnviar");
buttons.forEach(button => {
    button.disabled = true;
});
let buttonExt = false;
let buttonInt = false;

function goBack(){
    window.location.href = "/"
}

function stateHandle() {

    buttons.forEach(button => {
        button.disabled = buttonExt && buttonInt ? false : true;
    }); 
}
function showTextAndIconDownload(name) {
    var elem1 = document.createElement('img')
    elem1.src = "static/Assets/Icons/imgUpload.svg";
    var elem2 = document.createElement('label');
    elem2.setAttribute('id', `img-arquivo`);
    elem2.innerHTML = name;
    elem1.classList.add("icon-download");
    elem2.classList.add("icon-download");
    document.getElementsByClassName('arquivo')[0].appendChild(elem1);
    document.getElementsByClassName('arquivo')[0].appendChild(elem2);
}
function updateTextAndIcon(input, name) {
    let id = `img-label-${input}`;
    let imgLabel = document.querySelector("#" + id);
    imgLabel.innerHTML = name;
}
function showTextAndIcon(input, name) {
    var elem1 = document.createElement('img')
    var elem2 = document.createElement('label');
    elem2.setAttribute('id', `img-label-${input}`);
    elem2.innerHTML = name;
    elem1.classList.add("icon-upload");
    elem2.classList.add("label-icon-upload");
    if (input == "externa") {
        document.getElementsByClassName('imgExtIconContainer')[0].appendChild(elem1);
        document.getElementsByClassName('imgExtIconContainer')[0].appendChild(elem2);
    }
    else {
        document.getElementsByClassName('imgIntIconContainer')[0].appendChild(elem1);
        document.getElementsByClassName('imgIntIconContainer')[0].appendChild(elem2);
    }
}

function readImage() {
    if (this.files && this.files[0]) {
        if(validateFormat(this.files[0].name)){
            var file = new FileReader();
            file.onload = function(e) {
                document.getElementById("preview").src = e.target.result;
            };
            file.readAsDataURL(this.files[0]);
        }
    }
}
document.getElementById("imgButtonExt").addEventListener("change", readImage, false);

function readImage2() {
    if (this.files && this.files[0]) {
        if(validateFormat(this.files[0].name)){
            var file = new FileReader();
            file.onload = function(e) {
                document.getElementById("previews").src = e.target.result;
            };
            file.readAsDataURL(this.files[0]);
        }
    }
}
document.getElementById("imgButtonInt").addEventListener("change", readImage2, false);