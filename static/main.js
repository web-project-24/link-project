$(document).ready(function () {
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
});
function save() {
    alert("!!");
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
            alert(response["msg"])
            window.location.reload()
        }
    });
}