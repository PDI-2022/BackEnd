let body = {
    main:"",
    footer:"", 
    header:""
}
var applicationBody

function changeLimiarVermelho(input, type){

    if(type == 'range'){
        var red = document.querySelector(`#processing-${input}-limit`);
        var divCor = document.querySelector(`#cor-${input}-limit`);
        divCor.style.background = `rgb(${red.value}, 0, 0)`;
        var number = document.querySelector(`#numero-${input}-limit`);
        number.value = red.value;
    }
    else if(type == "number"){
        var red = document.querySelector(`#numero-${input}-limit`);
        var divCor = document.querySelector(`#cor-${input}-limit`);
        divCor.style.background = `rgb(${red.value}, 0, 0)`;
        var range = document.querySelector(`#processing-${input}-limit`);
        range.value = red.value
    }

}

function getPageBody(){
    body.main = document.querySelector("main")
    body.footer = document.querySelector("footer")
    body.header = document.querySelector("header")
}

window.onload = async function () {
    await auth()
    let imgFormatsView = document.querySelector("#img-formats")
    imgFormatsView.innerHTML = `Formatos aceitos: ${validFormatsImgs.map(img=>" " + img)}`
    getPageBody()

    localStorage.clear();

    // Esconde o select dos modelos
    let modelHolder = document.querySelector(".modelHolder")
    modelHolder.style.display = "none"

    // Esconde os inputs dos limiares de processamento
    changeLimiarVermelho('inf')
    changeLimiarVermelho('sup')
    let processingSupLimit = document.querySelector("#menu-processing-sup-limit")
    let processingInfLimit = document.querySelector("#menu-processing-inf-limit")
    processingSupLimit.style.display = "none" 
    processingInfLimit.style.display = "none"

    let menuClassificationSeedsClassNumber = document.querySelector("#menu-classification-seeds-class-number")
    // hideClassificationInputClass()
    menuClassificationSeedsClassNumber.style.display = "none"
    

    clickHandleModel()
    clickHandleProcessing()

}

function returnHome(){
    window.location.href = '/'
}

function sendToInicio() {
    window.location.href = '/#inicio'
}

function dragOverHandler(event, input) {
    event.preventDefault();
}

async function sendToBack() {
    await auth()
    let displayClassificationInfos = document.querySelector("#InputClass").checked
    let generatePageWithImages = document.querySelector("#InputPagaWithImages").checked
    let chooseLimiar = document.querySelector("#processing-seeds-classification").checked
    let limSup = chooseLimiar ? document.querySelector("#processing-sup-limit").value : 190
    let limInf = chooseLimiar ? document.querySelector("#processing-inf-limit").value : 168
    
    let seedsClassNumberInput = displayClassificationInfos ? document.querySelector("#menu-classification-seeds-class-number-input").value : 7

    let classificationYolo = document.querySelector("#classification-seeds-yolo").checked
    localStorage.setItem("classificationYolo",classificationYolo)

    if(seedsClassNumberInput > 7 || seedsClassNumberInput < 1){
        window.alert(`O valor do n??mero de classes deve ser maior que 1 e menor que 7. Valor atual ${seedsClassNumberInput} `)
        return
    }

    if(limSup < 91 || limSup > 255){
        window.alert(`O valor do limite superior deve ser maior que 91 e menor que 255. Valor atual ${limSup} `)
        return
    }
    else if(limSup.toString().includes(".") || limSup.toString().includes(",")){
        window.alert(`O valor do limite superior deve ser inteiro ${limSup} `)
        return
    }
    if(limInf < 91 || limInf > 255){
        window.alert(`O valor do limite inferior deve ser maior que 91 e menor que 255. Valor atual ${limInf} `)
        return
    }
    else if(limInf.toString().includes(".") || limInf.toString().includes(",")){
        window.alert(`O valor do limite inferior deve ser inteiro ${limInf} `)
        return
    }

    let seedTogether= document.querySelector("#pre-processing-seeds-division").checked

    let modelId = displayClassificationInfos ? document.querySelector("select").value : -1
    var tableAux = 0
    if(displayClassificationInfos){
        localStorage.setItem("hasClass",displayClassificationInfos)
    }
    if(!!json["interna"] && !!json["externa"]){
        var req = new XMLHttpRequest();
        req.timeout = 10 * 60 * 1000;
        const url = processUrl
        req.open('POST',url,true);
        req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
        let token = document.cookie
        token = token.split(`token=`)[1]
        req.setRequestHeader("token", `${token}`);

        data = {
            "displayClassificationInfos":displayClassificationInfos,
            "modelId":modelId,
            "generatePageWithImages":generatePageWithImages,
            "chooseLimiar":chooseLimiar,
            "limSup":limSup,
            "limInf":limInf,
            "seedTogether":seedTogether,
            "classificationYolo":classificationYolo,
            "internalImg":json["interna"],
            "externalImg":json["externa"],
            "seedsClassNumberInput":seedsClassNumberInput
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

                var showIconAndName = false
                if (!localStorage.getItem('csv')) {
                    showIconAndName = true;
                }
                if(localStorage.getItem('csv') != '' && tableAux == 0){

                    if(generatePageWithImages){
                        $('#modal-comp').modal('hide');

                        $('#modal-redirecting').modal({
                            show:true,
                            backdrop: 'static',
                            keyboard: false
                        })
                        window.location.href = "/seeds"
                        
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

async function generateDownloadScreen(){
    if(localStorage.getItem("classificationYolo") == "true"){
        let token = document.cookie
        token = token.split(`token=`)[1]
        let respEmbriao = await fetch(getEmbriaoCSVUrl, {
            method:"GET", 
            headers:{
                "token":`${token}`
            } 
        }).catch(err=>{
            console.error(err)
        })
        let csvembriao = await respEmbriao.text()
        localStorage.setItem("embriaoCsv",csvembriao)
        $('#modal-comp').modal('hide');
    }
    else{
        $('#modal-comp').modal('hide');
    }

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
        link.setAttribute("download", "Sementes.csv");
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    }
    if(!!localStorage.getItem("embriaoCsv")){
        const csvString = localStorage.getItem("embriaoCsv");
        var blob = new Blob([csvString], { type: 'text/plain;charset=utf-8;' });
        var link = document.createElement("a");
        if (link.download !== undefined) {
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", "Embriao.csv");
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }  
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