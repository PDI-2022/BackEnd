class Header extends HTMLElement {
    connectedCallback() {
        this.innerHTML = `
        <nav class="navbar navbar-light  d-flex justify-content-center" style="background-color: #712F26;">
            <a class="navbar-brand" onclick="returnHome()" style="display: flex; cursor: pointer;">
                <img src="/static/Assets/Logo/logo.svg" width="30" height="30" class="d-inline-block align-top" alt="">
                <div style="color: white; padding-left: 12px;">TetraSeed </div>
            </a>
        </nav>
        <div style="background-color: #fff; padding: 6px 0;"></div>
          `
    }
}
class Footer extends HTMLElement {
    connectedCallback() {
        this.innerHTML = ` 
        <footer class="page-footer font-small blue pt-4">
          <div class="container-fluid text-center text-md-left">
                <hr class="line"/>
                <div>
                    <h6>Projeto desenvolvido pela equipe de Interface na disciplina de PDI 2022 - UFC</h6>
                </div>
                <div class="row"> 
                    <div class="col-4">
                    </div>
                    <div class="col-2">
                        <h6>Contato</h6>
                    </div>
                    <div class="col-2">
                        <h6>Suporte</h6>
                    </div>
                    <div class="col-4"></div>
                </div>
            </div>
        </footer>
      `
    }
}
class ModalLoading extends HTMLElement {
    connectedCallback() {
        this.innerHTML = ` 
        <div class="modal" id="modal-comp" role="dialog">
            <div style="width: 100vw;height: 100%;">
                <div class="modal-content" style="height: 100%;background:rgba(247, 212, 212, 0.7)">
                    <div class="modal-body">
                        <div  style="display: flex;
                        width: 100%;
                        height: 100%;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;">
                            <div class="col-md-4 offset-md-4" style="    display: flex;
                            align-items: center;justify-content: center;margin-left:0 !important">
                                <div class="spinner-border" style="border: none;
                                border-top: .55em dotted #AE1E1E;
                                border-left: .45em dotted #AE1E1E;
                                border-right: .35em dotted #AE1E1E;
                                border-bottom: .25em dotted #AE1E1E;
                                width:150px;
                                height:150px;
                                animation: 3.25s linear infinite spinner-border;"
                                ></div>
                                <h3 id="modal-alert" class="form-text" style="color:#AE1E1E; margin-left:12px">
                                    Carregando...
                                </h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      `
    }
}

class ModalRedirecting extends HTMLElement {
    connectedCallback() {
        this.innerHTML = ` 
        <div class="modal" id="modal-redirecting" role="dialog">
            <div style="width: 100vw;height: 100%;">
                <div class="modal-content" style="height: 100%;background:rgba(247, 212, 212, 0.7)">
                    <div class="modal-body">
                        <div  style="display: flex;
                        width: 100%;
                        height: 100%;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;">
                            <div class="col-md-4 offset-md-4" style="    display: flex;
                            align-items: center;justify-content: center;margin-left:0 !important">
                                <div class="spinner-border" style="border: none;
                                border-top: .55em dotted #AE1E1E;
                                border-left: .45em dotted #AE1E1E;
                                border-right: .35em dotted #AE1E1E;
                                border-bottom: .25em dotted #AE1E1E;
                                width:150px;
                                height:150px;
                                animation: 3.25s linear infinite spinner-border;"
                                ></div>
                                <h3 id="modal-alert" class="form-text" style="color:#AE1E1E; margin-left:12px">
                                    Redirecionando...
                                </h3>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      `
    }
}

class DownloadPage extends HTMLElement {
    connectedCallback() {
        this.innerHTML = ` 
        <section style="flex-direction: column;align-items: center;">
            <div class="img-titles flex">
                <h2 class="img-title">Seu download está <span class="red-text">Pronto</span> !</h2>
            </div>
            <download-section></download-section>
        </section>
      `
    }
}

class DownloadSection extends HTMLElement {
    connectedCallback() {
        this.innerHTML = ` 
        <section class="container-section">
            <div class="container">
                <div class="mt-5 botao defaultButton">
                    <button type="button" class="btn btn-danger btn-lg" id="botaoDownload" onclick="downloadCsv()">Download</button>
                    <div class="arquivo"></div>
                </div>
                <div class="mt-5 botao defaultButton white">
                    <button 
                        type="button" 
                        class="btn btn-secondary btn-lg botaoVoltar" 
                        data-toggle="tooltip" 
                        data-placement="right" 
                        title="Clique aqui para voltar a tela de envio de imagens"
                        onclick="goBack()"
                    >
                        Voltar
                    </button>
                </div>
            </div>
        </section>
      `
    }
}

class ModalError extends HTMLElement {
    connectedCallback() {
        this.innerHTML = ` 
        <div class="modal" id="modal-erro" role="dialog">
            <div style="width: 100vw;height: 100%;">
                <div class="modal-content" style="height: 100%;background:rgba(247, 212, 212, 0.7)">
                    <div class="modal-body">
                        <div  style="display: flex;
                        width: 100%;
                        height: 100%;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;">
                            <div class="col-md-4 offset-md-4" style="    display: flex;
                            align-items: center;justify-content: center;margin-left:0 !important">
                                <img src="/static/Assets/Icons/cancel.svg">
                                <h3 id="modal-alert" class="form-text" style="color:#AE1E1E; margin-left:12px">
                                    Ops... Algo de errado aconteceu
                                </h3>
                            </div>
                            <a href="/" class="defaultButton">
                                <button type="button" class="btn btn-danger btn-lg botaoEnviar" >Voltar para o inicio </button>
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
      `
    }
}


customElements.define('main-header', Header);
customElements.define('main-footer', Footer);
customElements.define('modal-loading', ModalLoading);
customElements.define('modal-redirecting',ModalRedirecting);
customElements.define('modal-error', ModalError);
customElements.define('download-section', DownloadSection);
customElements.define('download-page', DownloadPage);



