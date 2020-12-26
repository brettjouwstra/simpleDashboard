$(document).ready(readyHandle);

function readyHandle(){

  console.log('jQuery is ready!');

  allFiles()
};

function allFiles(){
    html = '';
    img = "https://storage.googleapis.com/template-design/icons/svg_icons_big-list/icons/material/picture-as-pdf.svg";
    $.ajax({
        url: '/-/all',
        type: "GET",
        contentType: 'application/json',
        success: function(res) {
            parsed = JSON.parse(res)
            console.log(parsed)
            for (key in parsed) {
                value = parsed[key]
                console.log(value)
                html += `<button class="modal-btn" value="${value.referencename}" onclick="showModal(this.value)">
                <li><img src=${img}>${value.filename_original}</li>
                </button>`
            }
            $("#modal-holder").append(html)
        }
    })
};