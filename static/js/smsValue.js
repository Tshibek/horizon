function setNumber() {
    var x = document.getElementById("select-price").value;
    if (x == "1.23 zł") {
        document.getElementById("number").innerHTML = "71480";
        document.getElementById("addmoney-info").innerHTML = "1.23 zł";
    } else if (x == "2.46 zł") {
        document.getElementById("number").innerHTML = "72480";
        document.getElementById("addmoney-info").innerHTML = "2.46 zł";
    } else if (x == "3.69 zł") {
        document.getElementById("number").innerHTML = "73480";
        document.getElementById("addmoney-info").innerHTML = "3.69 zł";
    } else if (x == "4.92 zł") {
        document.getElementById("number").innerHTML = "74480";
        document.getElementById("addmoney-info").innerHTML = "4.92 zł";
    } else if (x == "6.15 zł") {
        document.getElementById("number").innerHTML = "75480";
        document.getElementById("addmoney-info").innerHTML = "6.15 zł";
    } else if (x == "7.38 zł") {
        document.getElementById("number").innerHTML = "76480";
        document.getElementById("addmoney-info").innerHTML = "7.38 zł";
    } else if (x == "11.07 zł") {
        document.getElementById("number").innerHTML = "79480";
        document.getElementById("addmoney-info").innerHTML = "11.07 zł";
    } else if (x == "17.22 zł") {
        document.getElementById("number").innerHTML = "91400";
        document.getElementById("addmoney-info").innerHTML = "17.22 zł";
    } else if (x == "23.37 zł") {
        document.getElementById("number").innerHTML = "91900";
        document.getElementById("addmoney-info").innerHTML = "23.37 zł";
    } else if (x == "24.60 zł") {
        document.getElementById("number").innerHTML = "92022";
        document.getElementById("addmoney-info").innerHTML = "24.60 zł";
    } else if (x == "30.75 zł") {
        document.getElementById("number").innerHTML = "92521";
        document.getElementById("addmoney-info").innerHTML = "30.75 zł";
    } else {
        document.getElementById("number").innerHTML = "BLAD: Nieznana cena!";
    }
}