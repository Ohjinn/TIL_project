$(document).ready(function () {
    getCards();
    showLocation();
});

window.addEventListener('load', () => {
    if (window.navigator.geolocation) {
        window.navigator.geolocation.getCurrentPosition(showLocation, showError)
    }
})

var myModal = document.getElementById('myModal')

myModal.addEventListener('showns.bs.modal', function () {
    myModal.focus()
})


function getCards() {
    $.ajax({
        type: "GET",
        url: `/sorted`,
        data: {},
        success: function (response) {
            velogCards = response['velogcards']
            tistoryCards = response['tistorycards']
            $("#velog-box").empty();
            velogCards.forEach(function (velogCards) {
                makeVelogCard(velogCards);
                makeModal(velogCards);

            });

            $("#tistory-box").empty();
            tistoryCards.forEach(function (tistoryCards) {
                makeTistoryCard(tistoryCards);
                makeModal(tistoryCards);
            });

        }
    })
}

function velClick() {
    if ($("#velog-box").is(":visible")) {
        $("#velog-box").hide();
    } else {
        $("#velog-box").show();
    }
}


function tisClick() {
    if ($("#tistory-box").is(":visible")) {
        $("#tistory-box").hide();
    } else {
        $("#tistory-box").show();
    }
}


function showLocation(position) {   // 위치 정보 호출 성공시
    let latitude = position.coords.latitude   // 위도
    let longitude = position.coords.longitude  // 경도
    let apiKey = '97329c7c315676010b49d9b9dc79185c';
    let weatherUrl = "https://api.openweathermap.org/data/2.5/weather?lat=" + latitude
        + "&lon=" + longitude
        + "&appid=" + apiKey;
    let options = {method: 'GET'}
    $.ajax(weatherUrl, options).then((response) => {
        console.log(response) // jSON 타입 위치 및 날씨 정보 로그 확인
        let icon = response.weather[0].icon
        let iconUrl = "http://openweathermap.org/img/wn/" + icon + ".png"
        let img = document.querySelector("#wicon")
        img.src = iconUrl
        let w_icon_id = icon[0] + icon[1];
        if (w_icon_id == '01') {
            $("#weather_comment").text("맑은 하늘이네요! 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '02') {
            $("#weather_comment").text("약간 구름낀 날씨네요! 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '03') {
            $("#weather_comment").text("구름이 조금 더 꼈지만 코딩 공부하기 좋은 날씨네요!♥");
        } else if (w_icon_id == '04') {
            $("#weather_comment").text("구름이 좀 끼고 우중충하니까 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '09') {
            $("#weather_comment").text("소나기가 내리는 지금은 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '10') {
            $("#weather_comment").text("비가 와요! 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '11') {
            $("#weather_comment").text("천둥 번개가 치는 지금은?! 코딩공부하기 좋은 날~♥");
        } else if (w_icon_id == '13') {
            $("#weather_comment").text("눈이 와요~! 코딩공부하기 좋은 날~♥");
        } else
            $("#weather_comment").text("안개가 낀 날씨도 역시! 코딩공부하기 좋은 날~♥");

        $("#tempr").text(Math.round(parseFloat((response.main.temp - 273))) + '˚'); // 현재 온도
    }).catch((error) => {
        console.log(error)
    })
}

function showError(position) {
    // 실패 했을 때 처리
    alert("위치 정보를 얻을 수 없습니다.")
}


function makeVelogCard(cards){
    let tempHtml = `<div class="card hotboxs ">
                         <img class="card-img-top card-rows" height="200" src="${cards['pic']}" alt="Card image cap">
                        <div class="card-body">
                            <h5 class="card-title">${cards['name']}</h5>
                            <p class="arrow_box">${cards['introduce']}</p>
                            <p class="card-text">${cards['url']}</p>
                            <div class="d-flex justify-content-center">
                            <a href="#" onclick="window.open('${cards['url']}', 'new')" class="btn btn-warning st">바로가기</a>
                            <button type="button" data-toggle="modal" data-target="#${cards['name']}"  class="btn btn-warning st">리뷰달기</button>
                        </div>
                        </div>
                    </div>`
    $("#velog-box").append(tempHtml);


}

$('#myModal').on('show.bs.modal', function (event) {
  let bookId = $(event.relatedTarget).data('test')
    console.log(bookId)
  // $(this).find('.modal-body input').val(bookId)
})

function makeTistoryCard(cards){
    let tempHtml = `<div class="card hotboxs">
                        <img class="card-img-top card-rows" height="200" src="${cards['pic']}" alt="Card image cap">
                        <div class="card-body">
                            <h5 class="card-title">${cards['name']}</h5>
                            <p class="card-text">${cards['url']}</p>
                            <div class="d-flex justify-content-center">
                            <a href="#" onclick="window.open('${cards['url']}', 'new')" class="btn btn-warning st">바로가기</a>
<!--                            <button type="button" data-toggle="modal" data-target="#myModal" class="btn btn-warning st">리뷰달기</button>-->
                        </div>
                        </div>
                    </div>`
    $("#tistory-box").append(tempHtml);
}

//검색
function search() {
    let txt = $("#searchtxt").val()
    $.ajax({
        type: "GET",
        url: "/search?txt=" + txt,
        data: {},
        success: function (response) {
            $("#flush").empty();
            let tempHtml =``
            if (txt == response.name) {
                let tempHtml = `<div class="card hotboxs">
                        <img class="card-img-top card-rows" height="200" src="${response['pic']}" alt="Card image cap">
                        <div class="card-body">
                            <h5 class="card-title">${response['name']}</h5>
                            <p class="card-text">${response['url']}</p>
                            <div class="d-flex justify-content-center">
                            <a href="${response['url']}" class="btn btn-warning st">바로가기</a>
<!--                            <button type="button" data-toggle="modal" data-target="#myModal" class="btn btn-warning st">리뷰달기</button>-->
                        </div>
                        </div>
                    </div>
                    <button onclick="window.location.href = '/'" type="button" class="btn btn-primary ">메인으로</button>`
                $("#flush").append(tempHtml);
            }
            else {
                let tempHtml =`<button onclick="window.location.href = '/'" type="button" class="btn btn-primary">메인으로</button>`
                $("#flush").append(tempHtml);
            }
        }
    });
}

function makeModal(info){
            temp_html = `<div class="modal fade" id=${info['name']} tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                            <div class="modal-dialog modal-lg">
                                <div class="modal-content">
                                    <div class="modal-header">
                                        <h5 class="modal-title" id="exampleModalLabel">한 줄 리뷰 작성하기</h5>
                                    </div>
                                    <div class="modal-body">
                                        <form>
                                            <div class="form-group">
                                                <label for="recipient-name" class="col-form-label">작성자:</label>
                                                <input type="text" class="form-control" id="writer${info['name']}">
                                            </div>
                                            <div class="form-group">
                                                <label for="message-text" class="col-form-label">리뷰를 달아주세요:</label>
                                                <textarea class="form-control" id="reviewcontent${info['name']}"></textarea>
                                            </div>
                                        </form>
                    
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-dismiss="modal">닫기</button>
                                        <button type="button" onclick="postReview('${info['name']}')" class="btn btn-warning">작성 완료</button>
                                    </div>
                                </div>
                            </div>
                        </div>`
            $("#set_modal").append(temp_html)
        }

//리뷰
function postReview(owner_name) {
    let writer = $('#writer'+owner_name).val()
    let review_content = $('#reviewcontent'+owner_name).val()
    console.log(owner_name, writer, review_content)
    $.ajax({
        type: "POST",
        url: "/review",
        data: {owner_give:owner_name, user_give:writer, review_give:review_content},
        success: function (response) {
            alert(response["msg"]);
            window.location.reload();

        }
    })
}

function getTarget(name) {

    alert(name)
    // $.ajax({
    //     type: "POST",
    //     url: "/review",
    //     data: {target_give: name},
    //     success: function (response) {
    //     }
    // })
}

function reset() {
    location.reload();
}