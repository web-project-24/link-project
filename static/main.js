$(document).ready(function () {
    //전체조회
    show_list();

    var fileTarget = $('.filebox .upload-hidden');

    fileTarget.on('change', function () {  // 값이 변경되면

        if (window.FileReader) {  // modern browser
            console.log(   $(this) )
            var filename = $(this)[0].files[0].name;
        } else {  // old IE
            var filename = $(this).val().split('/').pop().split('\\').pop();  // 파일명만 추출
        }
        // 추출한 파일명 삽입
        $(this).siblings('.upload-name').val(filename);
    });

    let i = 0;
    $("#btn").on("click", function () {

        console.log(i);
        if (i % 2 == 0) {
            $('#link-box').css("display", "none")
        } else {
            $('#link-box').css("display", "block")
        }
        i++;
    })
});
// 전체리스트 뿌리기
function show_list() {
    $.ajax({
        type: "GET",
        url: "/api/link",
        data: {},
        success: function (response) {
            let rows = response['linklist']
            for(let l=0; l < rows.length;l++){
                let sendMsg = rows[l];
                let id = rows[l]['id'];
                let image = rows[l]['image'];
                let tag = rows[l]['tag']
                let title = rows[l]['title']
                let url = rows[l]['url']
                let author = rows[l]['author']

                // if(done == 0 ){
                let temp_html = ``;
                 temp_html=`
                    <div class="response-box">
                        <div class="box${id}">
                            <div class="response-image">
                                <image src="${image}" alt="${title}" style="width: 100%" />
                            </div>
                        <div>
                            <p class="response-text">${title} id:${id}</p>
                            <p class="response-text">
                                <a href="${url}">
                                ${url}</a>
                            </p>
                            <p class="response-text">${tag}</p>
                            <p class="response-text">${author}</p>
                        </div>
                        <div class="btn-wrapper">
                            <button class="delete-btn btn-hover">삭제</button>
                            <button onclick="reTouchbtn( ${id} )" class="retouch-btn btn-hover">수정</button>
                        </div>
                        </div>
                        <div id="retouch_${id}" style="display: none">
                            <div class="filebox">
                                <input class="upload-name${id}" value="업로드 이미지 선택" disabled="disabled">
                                <label for="ex_filenames${id}">업로드</label>
                                <input type="file" id="ex_filenames${id}" style="position: inherit" onchange="fileUpload(this,${id})">
                            </div>
                            <input type="text" class="form-control submit-text title_retouch${id}"  placeholder="제목" value="${title}">
                            <input type="text" class="form-control submit-text url_retouch${id}"  placeholder="링크" value="${url}">
                            <input type="text" class="form-control submit-text author_retouch${id}" placeholder="작성자" value="${author}">
                            <input type="text" class="form-control submit-text tag_retouch${id}" placeholder="태그" value="${tag}">
                            <button onclick="saveRetouch(${id})" type="button" class="save-btn btn-hover save_btn_retouch save_btn_retouch${id}">저장</button>
                            <button onclick="cancel( ${id} )" type="button" class="save-btn btn-hover save_btn_retouch">취소</button>
                        </div>
                    </div>
                `
                $('#temp-box').append(temp_html);
            }
        }
    });
}
// 링크작성하기 저장기능
function save() {
    let title = $('#title').val()
    let url = $('#url').val()
    let tag = $('#tag').val()
    let author = $('#author').val()
    let image = $('#ex_filename')[0].files[0] // id file의 0번째 태그의 files 중 0 번째 파일
    console.log("image " ,image);
    let form_data = new FormData()

    form_data.append("title", title)
    form_data.append("url", url)
    form_data.append("tag", tag)
    form_data.append("image", image)
    form_data.append("author", author)

    for (let value of form_data.values()) {
        console.log(value);
    }

    // $.ajax({
    //     type: "POST",
    //     url: "/api/link",
    //     data: form_data,
    //     // 파일을 보내는데 필요한 기본 세팅이 되어있지 않을 수 있기 떄문에 false로 설정
    //     cache: false,
    //     contentType: false,
    //     processData: false,
    //     success: function (response) {
    //         alert(response)
    //         window.location.reload()
    //     }
    // });
}

//수정클릭
function reTouchbtn(idx){
    $(`.box${idx}`).css("display", "none")
    $(`#retouch_${idx}`).css("display", "block")
}

//수정클릭시 취소
function cancel(idx){
    $(`.box${idx}`).css("display", "block")
    $(`#retouch_${idx}`).css("display", "none")
}

// 수정에 필요한 파일업로드기능
function fileUpload(fis,id) {
    if (window.FileReader) {
        var str = fis.value;
        let filename= fis.files[0].name;
        $(`.upload-name${id}`).val(filename);
        console.log("fis.files[0] : ",fis.files[0]);
    }
}
//수정시 저장기능
function saveRetouch(id) {
    let title_modify = $(`.title_retouch${id}`).val()
    let author_modify = $(`.author_retouch${id}`).val()
    let url_modify = $(`.url_retouch${id}`).val()
    let tag_modify = $(`.tag_retouch${id}`).val()
    let image_modify = $(`#ex_filenames${id}`)[0].files[0]
    console.log("image_modify : ",image_modify);

    let form_data = new FormData()
    form_data.append("title", title_modify)
    form_data.append("url", url_modify)
    form_data.append("tag", tag_modify)
    form_data.append("image", image_modify)
    form_data.append("author", author_modify)

    for (let value of form_data.values()) {
        console.log(value);
    }

    $.ajax({
        type: "PUT",
        url: `/api/link/${id}`,
        data: form_data,
        // 파일을 보내는데 필요한 기본 세팅이 되어있지 않을 수 있기 떄문에 false로 설정
        cache: false,
        contentType: false,
        processData: false,
        success: function (response) {
            alert(response)
            window.location.reload()
        }
    });
}