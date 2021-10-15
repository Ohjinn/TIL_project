$(document).ready(function () {

    $.ajax({
        type: "GET",
        url: '/order',
        data: {},
        success: function (order) {
            $("#rank").empty();
            let Olist = order["orderlist"];
            console.log(Olist)
            for (let i = 0; i < 3; i++) {
                let tempHtml = ` <tr>
                      <td>${i + 1} . </td>
                      <td>${Olist[i]['name']}</td>
                      <td>님</td>
                      </tr> `;
                $("#orderrank").append(tempHtml);
            }
        }, error: function () {
            alert("오류")
        }
    });

    getCards();
    showLocation();

    $('#loginModalId').on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget)
        var modal = $(this)
        modal.find('.modal-title').text(recipient)
    })
});


window.addEventListener('load', () => {
    if (window.navigator.geolocation) {
        window.navigator.geolocation.getCurrentPosition(showLocation, showError)
    }
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
            });
            $("#tistory-box").empty();
            tistoryCards.forEach(function (tistoryCards) {
                makeTistoryCard(tistoryCards);
            });
            console.log(velogCards)
            console.log(tistoryCards)
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


function makeVelogCard(cards) {
    let tempHtml = `<div class="card hotboxs">
                         <img class="card-img-top card-rows" height="200" src="${cards['pic']}" alt="Card image cap">
                        <div class="card-body">
                            <h5 class="card-title">${cards['name']}</h5>
                            <p class="arrow_box">${cards['introduce']}</p>
                            <p class="card-text">${cards['url']}</p>
                            <div class="d-flex justify-content-center">
                            <a href="#" onclick="window.open('${cards['url']}', 'new')" class="btn btn-warning st">바로가기</a>
                            <a href="/review/${cards['id']}" onclick="showReviews()" class="btn btn-warning st">리뷰보기</a>
                        </div>
                        </div>
                    </div>`
    $("#velog-box").append(tempHtml);
}


function makeTistoryCard(cards) {
    let tempHtml = `<div class="card hotboxs">
                        <img class="card-img-top card-rows" height="200" src="${cards['pic']}" alt="Card image cap">
                        <div class="card-body">
                            <h5 class="card-title">${cards['name']}</h5>
                            <p class="arrow_box">${cards['introduce']}</p>
                            <p class="card-text">${cards['url']}</p>
                            <div class="d-flex justify-content-center">
                            <a href="#" onclick="window.open('${cards['url']}', 'new')" class="btn btn-warning st">바로가기</a>
                            <a href="/review/${cards['id']}" onclick="showReviews()" class="btn btn-warning st">리뷰보기</a>
                        </div>
                        </div>
                    </div>`
    $("#tistory-box").append(tempHtml);
}


//검색
function search() {
    let txt = $("#searchtxt").val()

    $.ajax({
        type: "PUT",
        url: "/search/" + txt,
        data: {},
        success: function (inc) {
            console.log(inc)
        }
    })
    $.ajax({
        type: "GET",
        url: "/search?txt=" + txt,
        data: {},
        success: function (response) {
            $("#flush").empty();
            console.log(response.name, txt);
            console.log(response.introduce);
            if (!response) {
                alert("올바른 값을 넣어주세요")
            } else {
                let tempHtml = `<div class="card hotboxs">
                        <img class="card-img-top card-rows" height="200" src="${response['pic']}" alt="Card image cap">
                        <div class="card-body">
                            <h5 class="card-title">${response['name']}</h5>
                             <p class="arrow_box">${response['introduce']}</p>
                            <p class="card-text">${response['url']}</p>
                            <div class="d-flex justify-content-center">
                            <a href="${response['url']}" class="btn btn-warning st">바로가기</a>
                            <button type="button" data-toggle="modal" data-target="#${response['name']}"  class="btn btn-warning st">리뷰달기</button>
                        </div>
                        </div>
                    </div>
                    <button onclick="window.location.href = '/'" type="button" class="btn btn-primary ">메인으로</button>`
                $("#flush").append(tempHtml);
                var countt = response.countt + 1;

                console.log(response.countt);
            }
        }, error: function onError() {
            alert("올바른 값을 넣어주세요");
        }
    });
}


/*
로그인 관련 js코드
 */
function toggle_sign_up() {
    $("#sign-up-box").toggleClass("is-hidden")
    $("#div-sign-in-or-up").toggleClass("is-hidden")
    $("#btn-check-dup").toggleClass("is-hidden")
    $("#help-id").toggleClass("is-hidden")
    $("#find-password").toggleClass("is-hidden")
    $("#help-password").toggleClass("is-hidden")
    $("#help-password2").toggleClass("is-hidden")
    $("#register-hide").toggleClass("is-hidden")
    $("#log-in-hide").toggleClass("is-hidden")
    $("#myModalLoginLabel").toggleClass("is-hidden")
    $("#myModalSignupLabel").toggleClass("is-hidden")
}


function is_nickname(asValue) {
    var regExp = /^(?=.*[a-zA-Z])[-a-zA-Z0-9_.]{2,10}$/;
    return regExp.test(asValue);
}


function is_password(asValue) {
    var regExp = /^(?=.*\d)(?=.*[a-zA-Z])[0-9a-zA-Z!@#$%^&*]{8,20}$/;
    return regExp.test(asValue);
}


function check_dup() {
    let username = $("#input-username").val()
    console.log(username)
    if (username == "") {
        $("#help-id").text("아이디를 입력했는지 확인해주세요.").addClass("text-danger")
        $("#input-username").focus()
        return;
    }
    if (!is_nickname(username)) {
        $("#help-id").text("아이디의 형식을 확인해주세요. 영문과 숫자, 일부 특수문자(._-) 사용 가능. 2-10자 길이").addClass("text-danger")
        $("#input-username").focus()
        return;
    }
    $.ajax({
        type: "POST",
        url: "/sign_up/check_dup",
        data: {
            username_give: username
        },
        success: function (response) {

            if (response["exists"]) {
                $("#help-id").text("이미 존재하는 아이디입니다.").addClass("text-danger")
                $("#input-username").focus()
            } else {
                $("#help-id").text("사용할 수 있는 아이디입니다.").removeClass("text-danger").addClass("is-success")
            }
            $("#help-id").removeClass("is-loading")

        }
    });
}


function sign_up() {
    let username = $("#input-username").val()
    let password = $("#input-password").val()
    let password2 = $("#input-password2").val()
    let name = $("#name").val()
    let birth = $("#input4").val()
    let url = $("#blog-url").val()

    if ($("#help-id").hasClass("text-danger")) {
        alert("아이디를 다시 확인해주세요.")
        return;
    } else if (!$("#help-id").hasClass("is-success")) {
        alert("아이디 중복확인을 해주세요.")
        return;
    }

    if (password == "") {
        $("#help-password").text("비밀번호를 입력해주세요.").addClass("text-danger")
        $("#input-password").focus()
        return;
    } else if (!is_password(password)) {
        $("#help-password").text("비밀번호의 형식을 확인해주세요. 영문과 숫자 필수 포함, 특수문자(!@#$%^&*) 사용가능 8-20자").addClass("text-danger")
        $("#input-password").focus()
        return
    } else {
        $("#help-password").text("사용할 수 있는 비밀번호입니다.").removeClass("text-danger").addClass("is-success")
    }
    if (password2 == "") {
        $("#help-password2").text("비밀번호를 입력해주세요.").addClass("text-danger")
        $("#input-password2").focus()
        return;
    } else if (password2 != password) {
        $("#help-password2").text("비밀번호가 일치하지 않습니다.").addClass("text-danger")
        $("#input-password2").focus()
        return;
    } else {
        $("#help-password2").text("비밀번호가 일치합니다.").removeClass("text-danger").addClass("is-success")
    }
    $.ajax({
        type: "POST",
        url: "/sign_up/save",
        data: {
            username_give: username,
            password_give: password,
            name_give: name,
            birth_give: birth,
            url_give: url
        },
        success: function (response) {
            alert("회원가입을 축하드립니다!")
            window.location.replace("/")
        }
    });

}


function sign_in() {
    let username = $("#input-username").val()
    let password = $("#input-password").val()

    if (username == "") {
        $("#help-id-login").text("아이디를 입력했는지 확인해주세요.")
        $("#input-username").focus()
        return;
    } else {
        $("#help-id-login").text("")
    }

    if (password == "") {
        $("#help-password-login").text("비밀번호를 입력해주세요.")
        $("#input-password").focus()
        return;
    } else {
        $("#help-password-login").text("")
    }
    $.ajax({
        type: "POST",
        url: "/sign_in",
        data: {
            username_give: username,
            password_give: password
        },
        success: function (response) {
            console.log(response)
            if (response['result'] == 'success') {
                $.cookie('mytoken', response['token'], {path: '/'});
                window.location.href = "/"
            } else {
                alert(response['msg'])
            }
        }
    });
}


function sign_out() {
    $.removeCookie('mytoken', {path: '/'});
    alert('로그아웃!')
    window.location.href = "/"
}


function kakao_login() {
    location.href = 'https://kauth.kakao.com/oauth/authorize?client_id=bc448c49046a3ad8a4f89959546084b3&response_type=code&redirect_uri=http://localhost:5000/oauth'
}


function reset() {
    location.reload();
}