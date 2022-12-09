class Footer extends HTMLElement {
    connectedCallback() {
        this.innerHTML = ` 
        <a href="/">
        <span class="logo flex-row">
          <img
            src="/static/Assets/Logo/logo.svg"
            alt="logo"
          />
          <strong>Tetra</strong>
          <div>Seed</div>
        </span>
      </a>
      <nav>
        <a href="https://github.com/PDI-2022" target="_blank">
          <img
            src="/static/Assets/Icons/githubIcon.svg"
            alt=""
          />
        </a>
      </nav>
      `
    }
}
customElements.define('main-footer', Footer);
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
customElements.define('modal-loading', ModalLoading);

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
customElements.define('modal-redirecting',ModalRedirecting);

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
customElements.define('download-page', DownloadPage);

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
customElements.define('download-section', DownloadSection);

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
customElements.define('modal-error', ModalError);

class PaginationComponent extends HTMLElement {
    connectedCallback() {
        var page = this.hasAttribute("page")? this.getAttribute("page"): "-";
        this.innerHTML = ` 
        <section id="paginate">
            <div class="controls">
                <div class="first" onclick="changePage('first')">&lt;&lt;</div>
                <div class="prev" onclick="changePage('dec')">&lt;</div>
                <div>
                    <div class="numbers">
                        ${page}
                    </div>
                </div>
                <div class="next" onclick="changePage('inc')">&gt;</div>
                <div class="last" onclick="changePage('last')">&gt;&gt;</div>
            </div>
        </section>
      `
    }
}
customElements.define('custom-pagination',PaginationComponent);

class NavbarUser extends HTMLElement {
    connectedCallback() {
        const page = window.location.pathname
        this.innerHTML = `<nav class="navbar fixed-top navbar-expand-lg navbar-light logo" style="box-shadow:none!important;width: 100vw!important;">
        <a href="/" class="navbar-brand">
          <div style="display: flex">
            <img
              src="/static/Assets/Logo/logo.svg"
              style="width: 50px; height: 50px"
              alt="logo"
            />
            <div class="brandName"><strong>Tetra</strong>Seed</div>
          </div>
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul
              class="navbar-nav ml-auto float-right"
              style="margin-left: 10px"
            >
            ${page == "/" ? `
            <li class="nav-item">
                <a class="nav-link itensNavLink" href="#inicio">Inicio</a>
            </li>
            <li class="nav-item">
                <a class="nav-link itensNavLink" href="#sobre">Sobre</a>
            </li>
            <li class="nav-item">
                <a class="nav-link itensNavLink" href="#equipe">Equipe</a>
            </li>`: ``}

          ${page != "/" ? `
            <li class="nav-item">
                <a class="nav-link itensNavLink" href="/">Home</a>
            </li>`: ``}

              <li class="nav-item">
                <a class="nav-link itensNavLink" href="/uploadModel"
                  >Upload de modelo</a
                >
              </li>
              <li class="nav-item">
                <img onclick="logout()" src="/static/Assets/Icons/logout.svg" style="cursor: pointer;">
              </li>
            </ul>
          </div>
        </div>
      </nav>`
    }
}
customElements.define('navbar-user', NavbarUser);

class NavbarAdmin extends HTMLElement {
    connectedCallback() {
        const page = window.location.pathname
        this.innerHTML = `<nav class="navbar fixed-top navbar-expand-lg navbar-light logo" style="box-shadow:none!important;width: 100vw!important;">
        <a href="/" class="navbar-brand">
          <div style="display: flex">
            <img
              src="/static/Assets/Logo/logo.svg"
              style="width: 50px; height: 50px"
              alt="logo"
            />
            <div class="brandName"><strong>Tetra</strong>Seed</div>
          </div>
        </a>
        <button
          class="navbar-toggler"
          type="button"
          data-toggle="collapse"
          data-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="container-fluid">
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul
              class="navbar-nav ml-auto float-right"
              style="margin-left: 10px"
            >

              ${page == "/" ? `
                <li class="nav-item">
                    <a class="nav-link itensNavLink" href="#inicio">Inicio</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link itensNavLink" href="#sobre">Sobre</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link itensNavLink" href="#equipe">Equipe</a>
                </li>`: ``}

              ${page != "/" ? `
                <li class="nav-item">
                    <a class="nav-link itensNavLink" href="/">Home</a>
                </li>`: ``}
              
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle nav-link itensNavLink" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Menu dos Modelos
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown" style="background-color:#D64040;color:white">
                    <a class="dropdown-item" href="/uploadModel" style="color:white">Upload de modelo</a>
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item" href="/modelList" style="color:white">Listagem de modelos</a>
                </div>
              </li>
              <li class="nav-item dropdown">
                <a class="nav-link dropdown-toggle nav-link itensNavLink" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                    Menu dos Usuários
                </a>
                <div class="dropdown-menu" aria-labelledby="navbarDropdown" style="background-color:#D64040;color:white">
                    <a class="dropdown-item" href="/new-user" style="color:white">Novo Usuário</a>
                    <div class="dropdown-divider"></div>
                    <a class="dropdown-item" href="/userList" style="color:white">Listagem de usuários</a>
                </div>
              </li>
              <li class="nav-item">
                <img onclick="logout()" src="/static/Assets/Icons/logout.svg" style="cursor: pointer;">
              </li>

            </ul>
          </div>
        </div>
      </nav>`
    }
}
customElements.define('navbar-admin', NavbarAdmin);

