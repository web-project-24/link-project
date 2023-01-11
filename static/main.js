$(document).ready(function () {
    //전체조회
    show_list();

    var fileTarget = $('.filebox .upload-hidden');

    fileTarget.on('change', function () {  // 값이 변경되면
        if (window.FileReader) {  // modern browser
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
// 전체리스트
function show_list() {
    $.ajax({
        type: "GET",
        url: "/api/link",
        data: {},
        success: function (response) {
            console.log(response);
            let rows = response['linklist']

            // for(let i=0; i < rows.length;i++){
            //     console.log(rows[i]);
            //     // let bucket = rows[i]['bucket']
            //     // let num = rows[i]['num']
            //     // let done = rows[i]['done']
            //
            //     // if(done == 0 ){
            //     // let temp_html = ``;
            //     // temp_html=`
            //     //     <li>
            //     //         <h2>✅ ${bucket}</h2>
            //     //         <button onclick="done_bucket(${num})" type="button" class="btn btn-outline-primary">완료!</button>
            //     //     </li>
            //         `
            //     //     temp_html=`
            //     //     <li>
            //     //         <h2>✅ ${bucket}</h2>
            //     //         <button onclick="done_bucket(${num})" type="button" class="btn btn-outline-primary">완료!</button>
            //     //     </li>
            //     //     `
            //     // }else {
            //     //     temp_html=`
            //     //     <li>
            //     //         <h2 class="done">✅ ${bucket}</h2>
            //     //     </li>
            //     //     `
            //     //
            //     // }
            //
            //     // $('#temp-box').append(temp_html);
            // }
        }
    });
}
function save() {
    let title = $('#title').val()
    let url = $('#url').val()
    let tag = $('#tag').val()
    let author = $('#author').val()
    let image = $('#ex_filename')[0].files[0] // id file의 0번째 태그의 files 중 0 번째 파일

    let form_data = new FormData()

    form_data.append("title", title)
    form_data.append("url", url)
    form_data.append("tag", tag)
    form_data.append("image", image)
    form_data.append("author", author)

    for (let value of form_data.values()) {
        console.log(value);
    }

    $.ajax({
        type: "POST",
        url: "/api/link",
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
function reTouchbtn(idx){
    $(`#retouch_${idx}`).append(`
            <div class="filebox">
                <input class="upload-name" value="업로드 이미지 선택" disabled="disabled">
                <label for="ex_filename">업로드</label>
                <input type="file" class="upload-hidden ex_filename_retouch">
            </div>
            <input type="text" class="form-control submit-text title_retouch"  placeholder="제목">
            <input type="text" class="form-control submit-text url_retouch"  placeholder="링크">
            <input type="text" class="form-control submit-text author_retouch" placeholder="작성자">
            <input type="text" class="form-control submit-text tag_retouch" placeholder="태그">
            <button onclick="save()" type="button" class="save-btn btn-hover save_btn_retouch">저장</button>
            <button type="button" class="save-btn btn-hover save_btn_retouch">취소</button>
    `);

    $(`.box${idx}`).css('display', 'none');
    // alert(idx);
    var fileTargets = $(`.retouch_${idx}.filebox .upload-hidden`);

    fileTargets.on('change', function () {  // 값이 변경되면
        if (window.FileReader) {  // modern browser
            var filename = $(this)[0].files[0].name;
        } else {  // old IE
            var filename = $(this).val().split('/').pop().split('\\').pop();  // 파일명만 추출
        }

        // 추출한 파일명 삽입
        $(this).siblings('.upload-name').val(filename);
    });

}

//#btn toggle

function cancel(idx){
    $(`.box${idx}`).css('display', 'black');
}